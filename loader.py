
# Подключаем встроенные модули и библиотеки:
import telebot
from dotenv import load_dotenv
from supabase import create_client
import os

# Нужная функция:
load_dotenv()

# Нужные переменные:
TOKEN = os.getenv("BOT_TOKEN")
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

bot = telebot.TeleBot(TOKEN)
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
