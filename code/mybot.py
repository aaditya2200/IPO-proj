import os
import telebot
from IPOscraper import IPOscraper
import urllib.request
import logging
import re

#API_KEY = os.getenv('API_KEY')
API_KEY ="1925784175:AAGlfZh7q6vkxpNXdpHr9HaCv1QcTn7keM4"

 #Setting up logger
logger = telebot.logger
telebot.logger.setLevel(logging.DEBUG) # Outputs debug messages to console.


knownUsers = []  # todo: cn we store this in reddis?
userStep = {}  # so they won't reset every time the bot restarts this can be removed when reading from db


bot = telebot.TeleBot(API_KEY)
stocks = []

def main():

    commands = {  # command description used in the "help" command
    'start'       : 'Get used to the bot',
    'help'        : 'Gives you information about the available commands',
    
}
    # error handling if user isn't known yet
# (obsolete once known users are saved to file, because all users
#   had to use the /start command and are therefore known to the bot)
    def get_user_step(uid):
        if uid in userStep:
            return userStep[uid]
        else:
            knownUsers.append(uid)
            userStep[uid] = 0
            print("New user detected, who hasn't used \"/start\" yet")
            return 0



    
    @bot.message_handler(commands=['start'])
    def send_welcome(message):
        cid = message.chat.id
        if cid not in knownUsers:
            knownUsers.append(cid) ##replace with reddis
            userStep[cid ]= 0
            bot.send_message(cid , "Hello New User!")
            command_help(message)
        else:
            bot.send_message(cid ,"welcome back!")
        bot.send_message(message.chat.id, "Welcome to the IPO Checker Bot! I will get the latest IPOs in your country and show it to you! ")
        bot.send_message(message.chat.id,"These are the current active IPOs in India ->")
        bot.send_message(message.chat.id,str(IPOscraper()))
    


    ##Help
    @bot.message_handler(commands=['help'])
    def command_help(m):
        cid = m.chat.id
        help_text = "The following commands are available: \n"
        for key in commands:  # generate help text out of the commands dictionary defined at the top
            help_text += "/" + key + ": "
            help_text += commands[key] + "\n"
        bot.send_message(cid, help_text)  # send the generated help page







    ## request for links to all docs regarding that IPO stored in db.
    """  def doc_request(message):
        request = message.text.split()
        if len(request) < 2 or request[0].lower() not in "Docs":
            return False
        else:
            return True
    
    @bot.message_handler(func=doc_request)
    def send_docs(message):
        request = message.text.split()[1]
        ##logic for getting links to red-herring prospectus
        ##data = yf.download(tickers=request, period='5m', interval='1m')
        if data.size > 0:
            data = data.reset_index()
            data["format_date"] = data['Datetime'].dt.strftime('%m/%d %I:%M %p')
            data.set_index('format_date', inplace=True)
            print(data.to_string())
            bot.send_message(message.chat.id, data['Close'].to_string(header=False))
        else:
            bot.send_message(message.chat.id, "No data!?")
 """
    def echo_all(message):
        bot.send_message(message.chat.id,message.text)

    bot.polling()


if __name__ ==  '__main__':
    main()