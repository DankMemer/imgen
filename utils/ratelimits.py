try:
    import ujson as json
except ImportError:
    import json
from datetime import datetime, timedelta
from time import time
import requests
import rethinkdb as r
from flask import request, make_response, jsonify

from utils.db import get_db, get_redis

config = json.load(open('config.json'))


class RatelimitCache(object):
    def __init__(self, name='global', expire_time=timedelta(0, 1, 0)):
        self.expire_time = expire_time
        self.id = name

    def __getitem__(self, item):
        db = get_redis()
        c = db.hgetall(f'ratelimit-cache:{self.id}:{item}')
        previous = int(c['timestamp'])
        expiry = datetime.strptime(c['expire_time'], '%H:%M:%S')
        expiry = expiry - datetime(1900, 1, 1)
        if time() - previous < expiry.seconds:
            return int(c['data'])
        db.delete(f'ratelimit-cache:{self.id}:{item}')
        return 0

    def get(self, item):
        return self.__getitem__(item)

    def __contains__(self, item):
        return get_redis().exists(f'ratelimit-cache:{self.id}:{item}')

    def __setitem__(self, key, value):
        db = get_redis()
        old_timestamp = db.hget(f'ratelimit-cache:{self.id}:{key}', 'timestamp')
        if old_timestamp:
            data = {'data': value, 'timestamp': old_timestamp, 'expire_time': str(self.expire_time)}
        else:
            data = {'data': value, 'timestamp': int(time() * 1000), 'expire_time': str(self.expire_time)}

        db.hmset(f'ratelimit-cache:{self.id}:{key}', data)
        if db.ttl(f'ratelimit-cache:{self.id}:{key}') == -1:
            db.expire(f'ratelimit-cache:{self.id}:{key}', self.expire_time.seconds)

    def expires_at(self, item):
        db = get_redis()
        c = db.hgetall(f'ratelimit-cache:{self.id}:{item}')

        previous = int(c['timestamp'])
        expire = datetime.strptime(c['expire_time'], '%H:%M:%S') - datetime(1900, 1, 1)
        date = previous + (expire.seconds * 1000)
        return date

    def expires_in(self, item):
        db = get_redis()
        c = db.hgetall(f'ratelimit-cache:{self.id}:{item}')

        previous = int(c['timestamp'])
        expire = datetime.strptime(c['expire_time'], '%H:%M:%S') - datetime(1900, 1, 1)
        return int(previous + (expire.seconds * 1000) - (time() * 1000))

    def set(self, key, value):
        return self.__setitem__(key, value)


globalcache = RatelimitCache(expire_time=timedelta(0, 60, 0))


def ratelimit(func, cache=globalcache, max_usage=300):
    def wrapper(*args, **kwargs):
        auth = request.headers.get('authorization', None)
        key = r.table('keys').get(auth).run(get_db())
        if key['unlimited']:
            return make_response(
                (*func(*args, **kwargs), {'X-Global-RateLimit-Limit': 'Unlimited',
                                          'X-Global-RateLimit-Remaining': 'Unlimited',
                                          'X-Global-RateLimit-Reset': 2147483647}))
        if key['id'] in cache:
            usage = cache.get(key['id'])
            if usage < max_usage:
                cache.set(key['id'], usage + 1)
                try:
                    return make_response((*func(*args, **kwargs),
                                          {'X-Global-RateLimit-Limit': max_usage,
                                           'X-Global-RateLimit-Remaining': max_usage - usage - 1,
                                           'X-Global-RateLimit-Reset': cache.expires_at(key['id'])}))
                except TypeError:
                    return func(*args, **kwargs)
            else:
                ratelimit_reached = key.get('ratelimit_reached', 0) + 1
                r.table('keys').get(auth).update({"ratelimit_reached": ratelimit_reached}).run(get_db())
                if ratelimit_reached % 5 == 0 and 'webhook_url' in config:
                    requests.post(config['webhook_url'],
                                  json={"embeds": [{
                                      "title": f"Application '{key['name']}' ratelimited 5 times!",
                                      "description": f"Owner: {key['owner']}\n"
                                      f"Total: {ratelimit_reached}"}]})
                return make_response((jsonify({'status': 429, 'error': 'You are being ratelimited', 'global': True}), 429,
                                      {'X-Global-RateLimit-Limit': max_usage,
                                       'X-Global-RateLimit-Remaining': 0,
                                       'X-Global-RateLimit-Reset': cache.expires_at(key['id']),
                                       'Retry-After': cache.expires_in(key['id'])}))
        else:
            cache.set(key['id'], 1)
            try:
                return make_response((*func(*args, **kwargs), {'X-Global-RateLimit-Limit': max_usage,
                                                               'X-Global-RateLimit-Remaining': max_usage - 1,
                                                               'X-Global-RateLimit-Reset': cache.expires_at(key['id'])}))
            except TypeError:
                return func(*args, **kwargs)

    return wrapper


def endpoint_ratelimit(auth, cache=globalcache, max_usage=5):
    key = r.table('keys').get(auth).run(get_db())
    if key['unlimited']:
        return {'X-RateLimit-Limit': 'Unlimited',
                                     'X-RateLimit-Remaining': 'Unlimited',
                                     'X-RateLimit-Reset': 2147483647}
    if key['id'] in cache:
        usage = cache.get(key['id'])
        if usage < max_usage:
            cache.set(key['id'], usage + 1)
            return {'X-RateLimit-Limit': max_usage,
                    'X-RateLimit-Remaining': max_usage - usage - 1,
                    'X-RateLimit-Reset': cache.expires_at(key['id'])}
        else:
            ratelimit_reached = key.get('ratelimit_reached', 0) + 1
            r.table('keys').get(auth).update({"ratelimit_reached": ratelimit_reached}).run(get_db())
            if ratelimit_reached % 5 == 0 and 'webhook_url' in config:
                requests.post(config['webhook_url'],
                              json={"embeds": [{
                                  "title": f"Application '{key['name']}' ratelimited 5 times!",
                                  "description": f"Owner: {key['owner']}\n"
                                                 f"Total: {ratelimit_reached}"}]})
            return {'X-RateLimit-Limit': max_usage,
                    'X-RateLimit-Remaining': -1,
                    'X-RateLimit-Reset': cache.expires_at(key['id'],),
                    'Retry-After': cache.expires_in(key['id'])}
    else:
        cache.set(key['id'], 1)
        return {'X-RateLimit-Limit': max_usage,
                'X-RateLimit-Remaining': max_usage - 1,
                'X-RateLimit-Reset': cache.expires_at(key['id'])}
