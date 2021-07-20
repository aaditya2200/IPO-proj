import os
import telebot
from IPOscraper import IPOscraper
import json
import urllib.request

#API_KEY = os.getenv('API_KEY')
API_KEY ="1925784175:AAGlfZh7q6vkxpNXdpHr9HaCv1QcTn7keM4"


bot = telebot.TeleBot(API_KEY)
stocks = []

@bot.message_handler(commands=['start','help'])
def send_welcome(message):
    bot.send_message(message.chat.id, "Hello and welcome to the IPO Checker Bot! I will get the latest IPOs in your country and show it to you! ")
    bot.send_message(message.chat.id,"This is your first time using this bot!")
    bot.send_message(message.chat.id,IPOscraper())


def echo_all(message):
    bot.send_message(message.chat.id,message.text)

print("scrapping...")
bot.polling()