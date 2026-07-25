import os
import google.generativeai as genai
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

print(f"Token loaded: {TELEGRAM_TOKEN[:10]}...")

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("HeenaQueenBot Online hai 😊")

async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    response = model.generate_content(update.message.text)
    await update.message.reply_text(response.text)

print("Bot started...")
app = Application.builder().token(TELEGRAM_TOKEN).build()  # v20 syntax
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))
app.run_polling()
