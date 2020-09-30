import os
import redis
from time import time, sleep
import json

config = json.load(open('config.json'))

REDIS_PASSWORD = config.get('redis_password', '')
REDIS_ADDRESS = config.get('redis_address', 'localhost')
REDIS_PORT = config.get('redis_port', 6379)
REDIS_DB = config.get('redis_db', 1)

r = redis.Redis(password=REDIS_PASSWORD, host=REDIS_ADDRESS, port=REDIS_PORT, db=REDIS_DB, decode_responses=True)

while 1:
    for file in os.listdir('cache'):
        try:
            file_name, ext = file.split('.')
            expiry = int(r.get(f'expiry:{file_name}'))
        except (ValueError, TypeError):
            continue
        current = int(time())
        if current >= expiry + 3600:
            print(f'YEETING {file}')
            os.remove(f'cache/{file}')
            r.delete(f'expiry:{file_name}')
    for file in os.listdir('cache/avatars'):
        try:
            file_name, ext = file.split('.')
            expiry = int(r.get(f'expiry:avatar:{file_name}'))
        except (ValueError, TypeError):
            continue
        current = int(time())
        if current >= expiry + 3600:
            print(f'YEETING {file}')
            os.remove(f'cache/avatars/{file}')
            r.delete(f'expiry:avatar:{file_name}')
    sleep(60)
