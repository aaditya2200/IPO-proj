from core.constants import USER_AGENT_LIST
from bot_config import BotConfig
import random
import requests
import os
import telebot


class BotInterface:
    @staticmethod
    def get_request_params() -> dict:
        return {
            'User-Agent': random.choice(USER_AGENT_LIST)
        }

    @staticmethod
    def get_details(command):
        if not command or len(command) == 0:
            return 1
        header = BotInterface.get_request_params()
        res = requests.get(
            url=BotConfig.API_BASE_URL +os.getenv('TELEGRAM_API_KEY')+ '/' +command
        )
    
