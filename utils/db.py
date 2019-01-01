import json

import rethinkdb as r
import redis
from flask import g

config = json.load(open('config.json'))

RDB_ADDRESS = config['rdb_address']
RDB_PORT = config['rdb_port']
RDB_DB = config['rdb_db']

REDIS_ADDRESS = config.get('redis_address', 'localhost')
REDIS_PORT = config.get('redis_port', 6379)
REDIS_DB = config.get('redis_db', 1)


def get_db():
    if 'rdb' not in g:
        g.rdb = r.connect(RDB_ADDRESS, RDB_PORT, db=RDB_DB)
    return g.rdb


def get_redis():
    if 'redis' not in g:
        g.redis = redis.Redis(host=REDIS_ADDRESS, port=REDIS_PORT, db=REDIS_DB, decode_responses=True)
    return g.redis
