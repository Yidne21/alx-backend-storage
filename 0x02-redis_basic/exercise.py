#!/usr/bin/env python3
'''Module for how to use redis data storage
'''
import uuid
import redis
from functools import wraps
from typing import Callable, Union


def count_calls(method: Callable) -> Callable:
    '''Tracks the number of calls made to a method in a Cache class.
    '''
    @wraps(method)
    def invoker(*args):
        '''Invokes the given method after incrementing its call counter.
        '''
        if args[0]._redis.exists(method.__qualname__) == 0:
            args[0]._redis.set(method.__qualname__, 1)
        else:
            args[0]._redis.incr(method.__qualname__, 1)
        return method(*args)
    return invoker

    
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

    def get(
        self,
        key: str,
        fn: Callable = None,
        ) -> Union[str, bytes, int, float]:
        '''Retrieves a value from a Redis data storage.
        '''
        data = self._redis.get(key)
        return fn(data) if fn is not None else data

    def get_str(self, key: str) -> str:
        '''Retrieves a string value from a Redis data storage.
        '''
        return self.get(key, lambda x: x.decode('utf-8'))

    def get_int(self, key: str) -> int:
        '''Retrieves an integer value from a Redis data storage.
        '''
        return self.get(key, lambda x: int(x))
