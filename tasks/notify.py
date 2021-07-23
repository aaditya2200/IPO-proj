"""
    Notify users when a new IPO is available

"""
from core.constants import REDIS_HASHES, DATA_STR
from core.utils import return_as_datetime_object
from redis_conf import RedisConf
from scrapers.mybot import MyBot


def notify():
    print_count = 0
    redis_client = RedisConf.create_connection_to_redis_server(True)
    response_code, users_list = RedisConf.read_from_redis(redis_client, REDIS_HASHES['notifications'])
    if response_code == 1:
        print('❌ Unable to read from redis. ')
    if not users_list:
        print('❗ No users have opted for notifications.')
        return
    users_list = [str(i) for i in users_list]
    bot = MyBot.create_bot()
    if not bot:
        print('❗ Unable to create bot.')
        return
    response, data = RedisConf.read_from_redis(r_client=redis_client, hash_name=REDIS_HASHES['current_ipo_details'])
    if response == 1:
        print('❌ Cannot fetch details from redis')
        return
    if not data:
        print('❌ Cannot fetch details from redis')
        return
    for i in range(len(data)):
        item = data[i]
        today, date = return_as_datetime_object(item['Open'])
        if date == today:
            data_str = DATA_STR.format(
                item['Issuer Company'],
                item['Exchange'],
                item['Open'],
                item['Close'],
                item['Lot Size'],
                item['Issue Price (Rs)'],
                item['Issue Price (Rs. Cr.)']
            )
            for m_id in users_list:
                bot.send_message(m_id, '📈 Here are some IPOs that were listed today! If you want all listings,'
                                       ' please run /start')
            for m_id in users_list:
                bot.send_message(m_id, data_str)
    # print('✅ Notified {} users successfully'.format(len(users_list)))
    return
