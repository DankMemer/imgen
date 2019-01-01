import json

import rethinkdb as r
import redis
from flask import g

config = json.load(open('config.json'))

RDB_ADDRESS = config['rdb_address']
RDB_PORT = config['rdb_port']
RDB_DB = config['rdb_db']

REDIS_ADDRESS = config['redis_address'] if 'redis_address' in config else 'localhost'
REDIS_PORT = config['redis_port'] if 'redis_port' in config else 6379
REDIS_DB = config['redis_db'] if 'redis_db' in config else 1


def get_db():
    if 'rdb' not in g:
        g.rdb = r.connect(RDB_ADDRESS, RDB_PORT, db=RDB_DB)
    return g.rdb


def get_redis():
    if 'redis' not in g:
        g.redis = redis.Redis(host=REDIS_ADDRESS, port=REDIS_PORT, db=REDIS_DB, decode_responses=True)
    return g.redis
