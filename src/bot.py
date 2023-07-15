import telebot
import os

bot = telebot.TeleBot(os.environ['ANONYMOUS_BOT_TOKEN'], parse_mode='HTML')