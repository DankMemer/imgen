import json

import redis
import rethinkdb as r
from flask import g

config = json.load(open('config.json'))

RDB_ADDRESS = config['rdb_address']
RDB_PORT = config['rdb_port']
RDB_DB = config['rdb_db']


def get_db():
    if 'rdb' not in g:
        g.rdb = r.connect(RDB_ADDRESS, RDB_PORT, db=RDB_DB)
    return g.rdb


def get_redis():
    if 'redis' not in g:
        g.redis = redis.Redis(db=9)
    return g.redis
