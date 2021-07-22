"""
    This file contains the code for the task that gets details of an IPO.
"""
from core.constants import GREET_MESSAGE, REDIS_HASHES, DATA_STR
from redis_conf import RedisConf
from scrapers.mybot import MyBot


def fetch_ipo_details():
    # start the bot
    bot = MyBot.create_bot()
    redis_client = RedisConf.create_connection_to_redis_server(True)

    @bot.message_handler(commands=['start', 'help'])
    def send_welcome(message):
        bot.send_message(message.chat.id, GREET_MESSAGE)
        bot.send_message(message.chat.id, "This is your first time using this bot!")
        # bot.send_message(message.chat.id, IPOScraper.ipo_scraper())
        response, data = RedisConf.read_from_redis(r_client=redis_client, hash_name=REDIS_HASHES['current_ipo_details'])
        if response == 1:
            print('❌ Cannot fetch details from redis')
            return
        if not data:
            print('❌ Cannot fetch details from redis')
            return

        for i in range(len(data)):
            item = data[i]
            data_str = DATA_STR.format(
                item['Issuer Company'],
                item['Exchange'],
                item['Open'],
                item['Close'],
                item['Lot Size'],
                item['Issue Price (Rs)'],
                item['Issue Price (Rs. Cr.)']
            )
            bot.send_message(message.chat.id, data_str)
        # this gives you the data.

    print('👂 Listening for messages')
    bot.polling()

    print('\n✅ Fetch IPO Details completed successfully')
    return
