from redis_conf import RedisConf
from core.utils import return_as_datetime_object


def update_redis_hash(hash_name='current_ipo_details'):
    """
    This function will update our redis hashes, for example, if an IPO has expired, it will still remain
    in current_ipo_details, since we do not remove it. This will take care of that
    """
    redis_client = RedisConf.create_connection_to_redis_server(True)
    response_code, ipo_details = RedisConf.read_from_redis(redis_client, hash_name=hash_name)
    if response_code == 1:
        print('❌ Cannot read from redis.')
        return
    if not ipo_details:
        print('❌ No current IPOs available. Please run `fetch_and_store` task.')
        return
    for item in ipo_details:
        try:
            today, date = return_as_datetime_object(item['Close'])
            if date < today:
                RedisConf.delete_from_hash(redis_client, hash_name, item['Issuer Company'])
            if len(item['Lot Size']) == 0 or len([item['Issue Price (Rs)']]) == 0:
                RedisConf.delete_from_hash(redis_client, hash_name, item['Issuer Company'])
        except Exception as e:
            print('❌ Exception: ', e)
    print('✅ Successfully completed update_redis_hash task.')
    return
