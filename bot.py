import os
import telebot
import google.generativeai as genai
from rembg import remove
from PIL import Image
import io

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

bot = telebot.TeleBot(TELEGRAM_TOKEN)
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-pro')

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "नमस्ते! मैं तैयार हूँ 🔥\n/movie नाम - Movie info\nया कोई भी सवाल पूछो\nफोटो भेजो - bg remove कर दूंगा")

@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    file_info = bot.get_file(message.photo[-1].file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    
    img = Image.open(io.BytesIO(downloaded_file))
    output = remove(img)
    
    bio = io.BytesIO()
    output.save(bio, 'PNG')
    bio.seek(0)
    bot.send_photo(message.chat.id, bio)

@bot.message_handler(func=lambda message: True)
def handle_text(message):
    if message.text.startswith('/movie'):
        movie_name = message.text.replace('/movie', '').strip()
        prompt = f"{movie_name} movie ke baare me short info do"
    else:
        prompt = message.text
    
    response = model.generate_content(prompt)
    bot.reply_to(message, response.text)

bot.polling()
