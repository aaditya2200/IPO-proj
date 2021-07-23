import telebot
from scrapers.ipo_scraper import IPOScraper
from core.constants import BOT_TOKEN, GREET_MESSAGE


class MyBot:
    
    @staticmethod
    def create_bot():
        bot = telebot.TeleBot(BOT_TOKEN)
        return bot

    @staticmethod
    def bot_message_handler(message):
        bot = MyBot.create_bot()

        @bot.message_handler(commands=['start', 'help'])
        def send_welcome(message):
            bot.send_message(message.chat.id, GREET_MESSAGE)
            # TODO: what if its not?
            # bot.send_message(message.chat.id, "This is your first time using this bot!")
            bot.send_message(message.chat.id, IPOScraper.ipo_scraper())

    @staticmethod
    def echo_all(message):
        bot = MyBot.create_bot()
        bot.send_message(message.chat.id, message.text)
