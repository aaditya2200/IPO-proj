import redis

class RedisConf:
    @staticmethod
    def create_connection_to_redis_server(decode_responses=True):
        """
        Creates connection to redis server
        :param decode_responses: Allows for reading a cached object from redis and type cast it 
                                 to python types, if True
        """
        r_client = redis.Redis(
            host='localhost',
            port=6379,
            decode_responses=decode_responses,
            password=''
        )
        return r_client