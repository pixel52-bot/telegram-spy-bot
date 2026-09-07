import telebot
import os
TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)
