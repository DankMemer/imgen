import os
import redis
from time import time, sleep

r = redis.Redis(db=1, decode_responses=True)

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
