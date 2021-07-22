"""
    This file contains the code for the task that gets details of an IPO.
"""
from core.constants import GREET_MESSAGE, REDIS_HASHES, DATA_STR
from redis_conf import RedisConf
from scrapers.mybot import MyBot


def fetch_ipo_details():
    # command description used in the "help" command
    commands = {
        '/start': 'Get used to the bot\n',
        '/help': 'Lookup  available commands \n',
        'Docs CompanyName ': 'Gives red herring prospectus and other documentation if issued for "Company Name" \n',
        'Subscribe CompanyName': '<alpha version> allows you to get notifications regarding events in the IPOs '
                                 'timeline \n',
        '/Subscriptions': '<alpha> Show all companies you have subscribed to\n'
    }

    # start the bot
    bot = MyBot.create_bot()
    redis_client = RedisConf.create_connection_to_redis_server(True)

    @bot.message_handler(commands=['start'])
    def send_welcome(message):
        print('✅ Received command from {}'.format(message.chat.id))
        # Checking if new user or existing user ,data stored in Redis
        if RedisConf.check_if_exists(redis_client, str(message.chat.id), REDIS_HASHES['users']) == 1:
            bot.send_message(message.chat.id, GREET_MESSAGE)
            bot.send_message(message.chat.id, "This is your first time using this bot!")
            RedisConf.store_in_redis(redis_client, str(message.chat.id), str(message.chat.id), REDIS_HASHES['users'])
            command_help(message)
        else:
            print('{} is an existing user!'.format(message.chat.id))
            bot.send_message(message.chat.id, '✋✋ Welcome Back! \n')
            bot.send_message(message.chat.id, "To view commands: " + '/help \n Here are the current and upcoming IPOs')

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

    # Help
    @bot.message_handler(commands=['help'])
    def command_help(m):
        cid = m.chat.id
        help_text = "The following commands are available: \n"
        for key in commands:  # generate help text out of the commands dictionary defined at the top
            help_text += key + ": "
            help_text += commands[key] + "\n"
        bot.send_message(cid, help_text)  # send the generated help page

    # DOC Sharing handler
    # Should return link for red herring or zip file itself (approx 7mb)
    # def doc_req takes a message like so: Docs Zomato instead of /docs ...
    def doc_request(message):
        request = message.text.split()
        if len(request) < 2 and request[0].lower() not in "Docs":
            return False
        else:
            return True
        # if message type by use is Docs <<comany name>> then send_docs runs

    @bot.message_handler(func=doc_request)
    def send_docs(message):
        request = message.text.split()[1]
        # logic for getting links to red-herring prospectus should return no document if not available
        # dummy message for testing
        bot.send_message(message.chat.id, "dummy doc :" + request)
        # if we can send doc then we use bot.send_document else just a link

    # Subscriptions to IPO
    def sub_ipo(message):
        request = message.text.split()
        if len(request) < 2 and request[0].lower() not in "Docs":
            return False
        else:
            return True
        # if message type by use is Docs <<comany name>> then send_docs runs

    @bot.message_handler(func=sub_ipo)
    def add_ipo(message):
        request = message.text.split()[1]
        # logic
        # dummy message for testing
        bot.send_message(message.chat.id,
                         "you have subscribed to " + request) + "\n You will now recieve notifcations when events take place"
        # if we cant do subscription then atleast we need to show the timeline for that IPO ,ill look into it"

    @bot.message_handler(commands=['Subscriptions'])
    def command_show_subscriptions(m):
        cid = m.chat.id
        # for cid key in redis display all subscriptions
        bot.send_message(cid, "Your subscriptions are:")

    print('👂 Listening for messages')
    bot.polling()

    print('\n✅ Successfully completed the task.')
    return
