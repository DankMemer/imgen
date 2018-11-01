from datetime import datetime, timedelta
import json

from flask import abort, request


class KeyExpired(KeyError):
    pass


class RatelimitCache(object):
    def __init__(self, expire_time=timedelta(0, 1, 0)):
        self.expire_time = expire_time
        self.cache = {}

    def __getitem__(self, item):
        c = self.cache[item]

        now = datetime.now()
        if now - c['timestamp'] < c['expire_time']:
            return c['data']

        del self.cache[item]
        raise KeyExpired(item)

    def get(self, item):
        c = self.cache[item]

        now = datetime.now()
        if now - c['timestamp'] < c['expire_time']:
            return c['data']

        del self.cache[item]
        raise KeyExpired(item)

    def __contains__(self, item):
        try:
            self[item]
            return True
        except KeyError:
            return False

    def __setitem__(self, key, value):
        self.cache[key] = {
            'data': value,
            'timestamp': datetime.now(),
            'expire_time': self.expire_time
        }

    def set(self, key, value):
        self.cache[key] = {
            'data': value,
            'timestamp': datetime.now(),
            'expire_time': self.expire_time
        }


cache = RatelimitCache()


def get_config():
    try:
        with open('config.json') as config:
            data = json.load(config)
            if not isinstance(data, dict):
                print('config.json must have a dict as base')
                return {}
            else:
                return data
    except FileNotFoundError:
        print('config.json wasn\'t found in the current directory')
        return {}


def ratelimit(func, max_usage=5):
    def wrapper(*args, **kwargs):
        key = request.headers.get('authorization', None)
        try:
            if get_config().get('memer_key') == key:
                is_memer = True
            else:
                is_memer = False
        except KeyError:
            print('memer-key must exist in the config')
            raise KeyError
        if key in cache:
            usage = cache.get(key)
            if usage < max_usage and not is_memer:
                cache.set(key, usage + 1)
                return func(*args, **kwargs)
            elif usage >= max_usage and is_memer:
                return func(*args, **kwargs)
            else:
                abort(status=429)
        elif key not in cache and is_memer:
            return func(*args, **kwargs)
        else:
            cache.set(key, 1)
            return func(*args, **kwargs)

    return wrapper