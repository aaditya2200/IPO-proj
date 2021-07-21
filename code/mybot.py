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


bot = telebot.TeleBot(API_KEY)
stocks = []

def main():
    @bot.message_handler(commands=['start','help'])
    def send_welcome(message):
        bot.send_message(message.chat.id, "Hello and welcome to the IPO Checker Bot! I will get the latest IPOs in your country and show it to you! ")
        bot.send_message(message.chat.id,"These are the current active IPOs in India!")
        bot.send_message(message.chat.id,str(IPOscraper()))
    
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

    print("scrapping...")
    bot.polling()


if __name__ ==  '__main__':
    main()