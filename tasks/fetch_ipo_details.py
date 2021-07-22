"""
    This file contains the code for the task that gets details of an IPO.
"""
from core.constants import GREET_MESSAGE, REDIS_HASHES, DATA_STR
from redis_conf import RedisConf
from scrapers.mybot import MyBot


knownUsers = []  # todo: store in reddis

def fetch_ipo_details():
    
    commands = {  # command description used in the "help" command
    'start'       : 'Get used to the bot',
    'help'        : 'Gives you information about the available commands',
    
     }

    


    


    # start the bot
    bot = MyBot.create_bot()
    redis_client = RedisConf.create_connection_to_redis_server(True)

    @bot.message_handler(commands=['start'])
    def send_welcome(message):
        print('✅ Received command from {}'. format(message.chat.id))
        bot.send_message(message.chat.id, GREET_MESSAGE)
        if RedisConf.check_if_exists(redis_client, str(message.chat.id), REDIS_HASHES['users']) == 1:
            bot.send_message(message.chat.id, "This is your first time using this bot!")
        RedisConf.store_in_redis(redis_client, str(message.chat.id), str(message.chat.id), REDIS_HASHES['users'])
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


    ##Help
    @bot.message_handler(commands=['help'])
    def command_help(m):
        cid = m.chat.id
        help_text = "The following commands are available: \n"
        for key in commands:  # generate help text out of the commands dictionary defined at the top
            help_text += "/" + key + ": "
            help_text += commands[key] + "\n"
        bot.send_message(cid, help_text)  # send the generated help page

    #######DOC Sharing handler############
    #Should return link for red herring or zip file itself (approx 7mb)
    #def doc_req takes a message like so: Docs Zomato instead of /docs ...
    def doc_request(message):
        request = message.text.split()
        if len(request) < 2 or request[0].lower() not in "Docs":
            return False
        else:
            return True
    
    #if message type by use is Docs <<comany name>> then send_docs runs
    @bot.message_handler(func=doc_request)
    def send_docs(message):
        request = message.text.split()[1]
        ##logic for getting links to red-herring prospectus
        ##dummy message for testing
        bot.send_message(message.chat.id , "dummy doc")


    print('👂 Listening for messages')
    bot.polling()

    print('\n✅ Fetch IPO Details completed successfully')
    return
