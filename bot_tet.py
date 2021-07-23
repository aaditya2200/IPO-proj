from bot_config import BotConfig
import os

#key = os.getenv('TEELGRAM_API_KEY')
bot = BotConfig.create_bot('1909033670:AAG8Rz9IEanmZlznZfxwsI0xuuRvAp2CUhU')

@bot.message_handler(commands=['hello'])
def greet(message):
    bot.reply_to(message, "Yo whats up")

bot.polling()