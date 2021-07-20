import redis
import os

class RedisConf:
    @staticmethod
    def create_connection_to_redis_server(decode_responses=True):
        """
        Creates connection to redis server
        :param decode_responses: Allows for reading a cached object from redis and type cast it 
                                 to python types, if True
        """
        host = os.getenv('redis_host')
        port = os.getenv('redis_port')
        password = os.getenv('redis_password')
        r_client = redis.Redis(
            host='localhost' or host,
            port=6379 or port,
            decode_responses=decode_responses,
            password='' or password
        )
        return r_client