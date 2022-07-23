from pymongo import MongoClient
from flask import g
import os
import json

def get_mongo_cur():
    ''' return mongodb cursor'''
    return MongoClient(os.environ['MYAIR_MONGODB'])


def open_mongo_cur():
    ''' store mongodb cursor in the g'''
    g.mongo_cur = MongoClient(os.environ['MYAIR_MONGODB'])


def close_mongo_cur():
    ''' pop & close mongodb cursor in the g'''
    mongo_cur = g.pop('mongo_cur', None)
    if mongo_cur:
        mongo_cur.close()

def init_models():
    '''mongodb-init function'''
    cur = MongoClient(os.environ['MYAIR_MONGODB'])
    db_name = 'Myair'
    col_name = 'masterconfig'
    col = cur[db_name][col_name]

    with open('./app/models/db/region.json', encoding='UTF8') as f:
        data = json.load(f)

    col.update({'key': 'region'}, data, upsert=True)

    cur.close()
