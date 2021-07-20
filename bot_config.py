from telebot import TeleBot

class BotConfig:
    API_BASE_URL = 'https://api.telegram.org/bot'
    commands = ['hello']

    @staticmethod
    def create_bot(API_KEY):
        bot = TeleBot(API_KEY)
        return bot