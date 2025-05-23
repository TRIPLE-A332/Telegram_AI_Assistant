# Telegram AI Assistant 

Link to Bot - https://t.me/GeminiPoweredAssistant_bot 

A voice and text-based AI assistant for Telegram, powered by **Google Gemini (Generative AI)** and **OpenAI Whisper** for transcription.

---

## Features

- 🔊 Accepts voice messages (converted using Whisper)
- 💬 Accepts text messages
- 🧠 Responds with Gemini-powered smart answers
- 🌍 Globally accessible Telegram bot
- 🔐 Secure API token management via `.env` or `tokens.py`

---

## How It Works

1. User sends a voice or text message to the bot.
2. Voice messages are transcribed using `openai-whisper`.
3. The transcribed or typed prompt is sent to Gemini (`gemini-1.5-flash`).
4. The bot responds intelligently in real-time.

---

## Project Structure

├── bot_main.py # Main Telegram bot logic

├── .env # API keys (excluded from Git)

├── requirements.txt # Python dependencies

├── .gitignore # Git exclusions

├── README.md # Project documentation

## Install dependencies:

pip install -r requirements.txt

## Add your API keys in a tokens.py file:

GEMINI_TOKEN = "your-gemini-api-key"
BOT_TOKEN = "your-telegram-bot-token"

Or use a .env file with python-dotenv:

GEMINI_TOKEN=your-gemini-api-key
BOT_TOKEN=your-telegram-bot-token

