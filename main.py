import sys
from tasks.fetch_and_store_v2 import fetch_and_store_v2
from tasks.fetch_ipo_details import fetch_ipo_details
from tasks.notify import notify
from tasks.get_market_sentiment import get_market_sentiment
from tasks.get_rh_prospectus import get_rh_prospectus
from tasks.fetch_and_store import fetch_and_store
from tasks.update_redis_hash import update_redis_hash

available_commands = {
    'notify': {
        'name': 'notify',
        'help': '',
    },
    'fetch_ipo_details': {
        'name': 'fetch_ipo_details',
        'help': '',
    },
    'get_market_sentiment': {
        'name': 'get_market_sentiment',
        'help': '',
    },
    'get_rh_prospectus': {
        'name': 'get_market_prospectus',
        'help': '',
    },
    'fetch_and_store': {
        'name': 'fetch_and_store',
        'help':'',
    },
    'update_redis_hash': {
        'name': 'update_redis_hash',
        'help': '',
    },
}


def main(argv):
    if not len(argv) or argv[0] not in available_commands.keys():
        print('Available commands: ')
        for key, val in available_commands.items():
            print('-> {}: {}'.format(
                key, val['help']
            ))
        print('\n')
        return
    task_name = argv[0]
    if task_name == available_commands['notify']['name']:
        notify()
    elif task_name == available_commands['get_rh_prospectus']['name']:
        get_rh_prospectus()
    elif task_name == available_commands['get_market_sentiment']['name']:
        get_market_sentiment()
    elif task_name == available_commands['fetch_ipo_details']['name']:
        fetch_ipo_details()
    elif task_name == available_commands['fetch_and_store']['name']:
        fetch_and_store()
    elif task_name == available_commands['update_redis_hash']['name']:
        update_redis_hash()
    
    elif task_name == available_commands['fetch_v2']['name']:
        fetch_and_store_v2()

if __name__ == '__main__':
    main(sys.argv[1:])