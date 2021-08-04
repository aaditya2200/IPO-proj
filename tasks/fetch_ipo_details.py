"""
    This file contains the code for the task that gets details of an IPO.
"""
import json

from core.constants import GREET_MESSAGE, REDIS_HASHES, DATA_STR, V1_DATA_STR, PAYMENTS_LINK
from redis_conf import RedisConf
from scrapers.mybot import MyBot


def fetch_ipo_details():
    # command description used in the "help" command
    commands = {
        '/start': 'Get used to the bot\n',
        '/help': 'Lookup available commands \n',
        '/list': 'List all IPOs\n',
        '/list_v1': 'List IPOs which do not have an RHP doc\n',
        '/rhp': 'Use this command along with the company name. For example, /rhp zomato. You will receive the RHP '
                'documents related to that IPO. \n',
        '/donate': 'Donate 100 rupees if you like this service, it aids in paying for cloud services.\n',
        '/contribute': 'Contribute to this project!\n',
        '/contact': 'Contact information for feedback and queries.\n'
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
            bot.send_message(message.chat.id, '🖊 If you would like to see all IPOs, run /list')
            RedisConf.store_in_redis(redis_client, str(message.chat.id), str(message.chat.id), REDIS_HASHES['users'])
            command_help(message)
        else:
            print('{} is an existing user!'.format(message.chat.id))
            bot.send_message(message.chat.id, '✋✋ Welcome Back! \n')
            bot.send_message(message.chat.id, "To view commands, run " + '/help')
            bot.send_message(message.chat.id, '🖊 If you would like to see current and upcoming IPOs, run /list')

        # bot.send_message(message.chat.id, IPOScraper.ipo_scraper())
        # this gives you the data.

    # Help
    @bot.message_handler(commands=['help'])
    def command_help(m):
        print('✅ Received command from {}'.format(m.chat.id))
        cid = m.chat.id
        bot.send_message(cid, '📚 Welcome to bot help! You will find everything you need to get started over here! ')
        help_text = "🖊 The following commands are available: \n\n"
        for key in commands:  # generate help text out of the commands dictionary defined at the top
            help_text += key + ": "
            help_text += commands[key] + "\n"
        bot.send_message(cid, help_text)  # send the generated help page

    # DOC Sharing handler
    # Should return link for red herring or zip file itself (approx 7mb)
    # def doc_req takes a message like so: Docs Zomato instead of /docs ...
    def doc_request(message):
        request = message.text.split()
        if len(request) < 2 and request[0].lower() not in "RHP":
            return False
        else:
            return True
        # if message type by use is Docs <<comany name>> then send_docs runs

    @bot.message_handler(func=doc_request)
    def send_docs(message):
        ##connect to redis hash
        print('✅ Received command for RHP from {}'.format(message.chat.id))
        response, data = RedisConf.read_from_redis(r_client=redis_client, hash_name=REDIS_HASHES['ipo_details_v2'])
        if response == 1:
            print('❌ Cannot fetch RHP details from redis')
            return
        if not data:
            print('❌ Cannot fetch RHP details from redis')
            return

        request = message.text.split()[1:][0]
        # logic for getting links to red-herring prospectus should return no document if not available
        # dummy message for testing
        found = False
        for item in data:
            company_name_list = [word.lower() for word in item['Issuer Company'].split()]
            if request in company_name_list or request == item['Issuer Company']:
                found = True
                try:
                    val = item['Red Herring Prospectus']
                    bot.send_message(message.chat.id, val[2:-2])
                except Exception as e:
                    bot.send_message(message.chat.id, '❌ Could not find RHP details for this company.')
                    print(e)
            else:
                continue
            if not found:
                print('❌ Could not find company.')
        # if RedisConf.check_if_exists(redis_client, request, 'IPO_DETAILS_V2') == 0:
        #     print('❌ Could not find company. ')
        #     for key in data:
        #         if key['Issuer Company'] == request:
        #             bot.send_message(message.chat.id, key['Red Herring Prospectus'][1])
        #
        #         else:
        #             bot.send_message(message.chat.id, '❌ Could not find RH Prospectus for {}'.format(request))
        # else:
        #     bot.send_message(message.chat.id, '❌ Please enter a valid company name (Full as stated in \list): ')

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
                         f"you have subscribed to {request}") + "\n You will now recieve notifcations when events " \
                                                                "take place "
        # if we cant do subscription then atleast we need to show the timeline for that IPO ,ill look into it"

    @bot.message_handler(commands=['Subscriptions'])
    def command_show_subscriptions(m):
        cid = m.chat.id
        # for cid key in redis display all subscriptions
        bot.send_message(cid, "Your subscriptions are:")

    @bot.message_handler(commands=['notify'])
    def notify(message):
        print('✅ Received command from {}'.format(message.chat.id))
        message_id = message.chat.id
        if RedisConf.check_if_exists(redis_client, str(message_id), REDIS_HASHES['notifications']) == 0:
            bot.send_message(message_id, '❗ You have already opted for notifications! You will get an update whenever '
                                         'there is one. ')
        elif RedisConf.check_if_exists(redis_client, str(message_id), REDIS_HASHES['users']) == 0:
            RedisConf.store_in_redis(redis_client, str(message_id), str(message_id), REDIS_HASHES['notifications'])
            bot.send_message(message_id,
                             'Congratulations! 👏 You will now be notified whenever a new IPO is available!')

    @bot.message_handler(commands=['list'])
    def ipo_list(message):
        print('✅ Received command from {}'.format(message.chat.id))
        response, data = RedisConf.read_from_redis(r_client=redis_client, hash_name=REDIS_HASHES['ipo_details_v2'])
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
                item['Open'],
                item['Close'],
                item['Lot Size'],
                item['Issue Price'],
                item['Cost of 1 lot'],
                # item['Red Herring Prospectus']
            )

            bot.send_message(message.chat.id, data_str)

    @bot.message_handler(commands=['contribute'])
    def contribute(message):
        print('✅ Received command from {}'.format(message.chat.id))
        bot.send_message(message.chat.id, 'If you would like to contribute to this project, please visit this link: '
                                          'https://github.com/aaditya2200/IPO-proj')
        bot.send_message(message.chat.id, 'If there is anything we can change, let us know by sending an email. You '
                                          'can find contact info on GitHub. 📧📨')


    @bot.message_handler(commands=['donate'])
    def donate(message):
        bot.send_message(message.chat.id, '💰 You can donate an amount of 100 rupees at the below link. If you would like to donate an '
                                          'amount lesser or lower, please contact us. See /contact for more.')
        bot.send_message(message.chat.id, PAYMENTS_LINK)


    @bot.message_handler(commands=['contact'])
    def contact(message):
        bot.send_message(message.chat.id, 'mailto:oneipo941@gmail.com')

    @bot.message_handler(commands=['list_v1'])
    def list_all(message):
        print('✅ Received command from {}'.format(message.chat.id))
        response, data = RedisConf.read_from_redis(r_client=redis_client, hash_name=REDIS_HASHES['current_ipo_details'])
        if response == 1:
            print('❌ Cannot fetch details from redis')
            return
        if not data:
            print('❌ Cannot fetch details from redis')
            return
        for i in range(len(data)):
            item = data[i]
            data_str = V1_DATA_STR.format(
                item['Issuer Company'],
                item['Exchange'],
                item['Open'],
                item['Close'],
                item['Lot Size'],
                item['Issue Price (Rs)'],
                item['Issue Price (Rs. Cr.)']
            )
            bot.send_message(message.chat.id, data_str)


    print('👂 Listening for messages')
    bot.polling()

    print('\n✅ Successfully completed the task.')
    return
