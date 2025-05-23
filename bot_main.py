import os
import subprocess
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters
from telegram.ext import CommandHandler


import google.generativeai as genai
import json

from faster_whisper import WhisperModel
import requests

from dotenv import load_dotenv
import os

load_dotenv() 

GEMINI_TOKEN = os.getenv("GEMINI_TOKEN")
BOT_TOKEN = os.getenv("BOT_TOKEN")


genai.configure(api_key=GEMINI_TOKEN)
genai_model = genai.GenerativeModel("models/gemini-1.5-flash")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hi! I’m your AI assistant. You can send me a message or voice note and I’ll respond.")


async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_input = update.message.text
    await update.message.reply_text("Thinking...")
    response = call_gemini(user_input)
    
    reply = response.get("raw") if "raw" in response else response.get("reply", "Error.")
    await update.message.reply_text(reply)


def call_gemini(prompt: str) -> dict:
    try:
        chat = genai_model.start_chat(history=[])
        response = chat.send_message(prompt)
        return {"reply": response.text.strip()}
    except Exception as e:
        print("Gemini Error:", e)
        return {"error": str(e)}


# Load Whisper model once
model = WhisperModel("tiny", compute_type="int8") 

# Download voice file
async def download_voice_file(file_id: str, bot) -> str:
    file = await bot.get_file(file_id)
    ogg_path = "voice.ogg"
    await file.download_to_drive(ogg_path)

    wav_path = "voice.wav"
    # Convert ogg to wav using ffmpeg
    subprocess.run(["ffmpeg", "-y", "-i", ogg_path, wav_path], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return wav_path

# Handle voice message
async def handle_voice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    bot = context.bot
    file_id = update.message.voice.file_id

    await update.message.reply_text("Transcribing...")

    wav_file = await download_voice_file(file_id, bot)
    segments, _ = model.transcribe("voice.wav")
    transcription = " ".join(segment.text for segment in segments)

    await update.message.reply_text(f"You said: {transcription}\n Thinking...")

    response = call_gemini(transcription)
    reply = response.get("reply", response.get("error", "Error."))

    await update.message.reply_text(reply)



if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    app.add_handler(MessageHandler(filters.VOICE, handle_voice))

    print("Bot is running...")
    app.run_polling()
