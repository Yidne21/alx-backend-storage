#!/usr/bin/env python3
'''Module for how to use redis data storage
'''
import uuid
import redis
from typing import Union


class Cache:
    '''object representation of data to sore in redis storage
    '''
    def __init__(self) -> None:
        '''Initializes a Cache instance.
        '''
        self._redis = redis.Redis()
        self._redis.flushdb(True)

    def store(self, data:Union[str, bytes, int, float]) ->str:
        '''Store a value in a Redis data sorage and returns the key.
        '''
        data_key = str(uuid.uuid4())
        self._redis.set(data_key, data)
        return data_key

