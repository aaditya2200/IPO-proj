import json

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
        # password = os.getenv('redis_password')
        r_client = redis.Redis(
            host='localhost' or host,
            port=6379 or port,
            decode_responses=decode_responses,
            password=''
        )
        return r_client

    @staticmethod
    def store_in_redis(r_client, key, value, hash_name):
        """
        Stores the value with a key in redis. For optimal use, value should be json.dumps(value), so it can be used
        when it is retrieved
        :param r_client: Redis client, as returned by create_connection_to_redis_server(True)
        :param key: the str(issuer name)
        :param value: whatever we set it to
        :param hash_name: use REDIS_HASHES defined in core.constants, for example REDIS_HASHES['users']
        :return:
        """
        if not hash_name or not r_client:
            return 1
        response = r_client.hset(hash_name, key, value)
        if response:
            return 0
        else:
            return 1

    @staticmethod
    def read_from_redis(r_client, hash_name):
        """
        Reads data from redis, will return them in python usable form
        :param r_client: Redis client, as returned by create_connection_to_redis_server(True)
        :param hash_name: use REDIS_HASHES defined in core.constants, for example REDIS_HASHES['users']
        :return:
        """
        if not r_client or not hash_name:
            return 1
        response = r_client.hgetall(hash_name)
        if not response:
            return 1, {}
        data = [json.loads(item) for item in response.values()]
        return 0, data

    @staticmethod
    def check_if_exists(r_client, key, hash_name):
        """
        Check if a key exists in redis
        :param r_client: redis client
        :param key: to be found
        :param hash_name: use REDIS_HASHES defined in core.constants, for example REDIS_HASHES['users']
        :return:
        """
        if not r_client or not hash_name:
            return 1
        response = r_client.hexists(hash_name, key)
        if response == 1:
            return 0
        else:
            return 1

    @staticmethod
    def delete_from_hash(r_client, key, hash_name):
        """
        Deleted a key from a hash
        :param r_client: redis client
        :param key: to be deleted
        :param hash_name: use REDIS_HASHES defined in core.constants, for example REDIS_HASHES['users']
        :return:
        """
        if not r_client or not hash_name:
            return 1
        response = r_client.hdel(hash_name, key)
        if response == 1:
            return 0

