#!/usr/bin/env python3
'''Module of task 8
'''


def list_all(mongo_collection):
    '''List all document in a collection.
    '''
    return [doc for doc in mongo_collection.find()]
