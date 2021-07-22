from redis_conf import RedisConf
from core.constants import REDIS_HASHES
from core.utils import return_as_datetime_object


def update_redis_hash():
    """
    This function will update our redis hashes, for example, if an IPO has expired, it will still remain
    in current_ipo_details, since we do not remove it. This will take care of that
    """
    redis_client = RedisConf.create_connection_to_redis_server(True)
    response_code, ipo_details = RedisConf.read_from_redis(redis_client, hash_name=REDIS_HASHES['current_ipo_details'])
    if response_code == 1:
        print('❌ Cannot read from redis.')
        return
    if not ipo_details:
        print('❌ No current IPOs available. Please run `fetch_and_store` task.')
        return
    for item in ipo_details:
        today, date = return_as_datetime_object(item['Close'])
        if date < today:
            RedisConf.delete_from_hash(redis_client, REDIS_HASHES['current_ipo_details'], item['Issuer Company'])
    print('✅ Successfully completed update_redis_hash task.')
    return
