import telebot
import requests
import google.generativeai as genai
import os
from remove_bg import remove_bg_api

TOKEN = os.environ.get("TELEGRAM_TOKEN")
GEMINI_KEY = os.environ.get("GEMINI_KEY")
REMOVEBG_KEY = os.environ.get("REMOVEBG_KEY")
CLIPDROP_KEY = os.environ.get("CLIPDROP_KEY")

bot = telebot.TeleBot(TOKEN)
genai.configure(api_key=GEMINI_KEY)

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Heena Bot On hai 🔥\nText bhejo ya photo bhejo BG remove ke liye")

@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    bot.reply_to(message, "Photo aa gayi, BG remove kar raha hu...")

@bot.message_handler(func=lambda m: True)
def handle_text(message):
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content(message.text)
    bot.reply_to(message, response.text)

bot.polling()
