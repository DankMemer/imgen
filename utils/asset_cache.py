from io import BytesIO
from time import time

from PIL import ImageFont
from flask import g


class AssetCache(object):
    def __init__(self, expire_time=300, gc_interval=60):
        self._gc_loop = g.gc_loop
        self._last_gc = time()
        self._gc_interval = gc_interval
        self._expire_time = expire_time
        self._cache = {}

    @staticmethod
    def _run_gc(cache_obj):
        for key in list(cache_obj._cache):
            value = cache_obj._cache[key]
            if value['expiry'] < time():
                obj = cache_obj._cache.pop(key)
                # noinspection PyBroadException
                try:
                    obj['data'].close()
                except Exception:
                    pass

    def __getitem__(self, item):
        now = time()
        if self._last_gc + self._gc_interval < now:
            self._gc_loop.call_soon_threadsafe(self._run_gc, self)
            self._last_gc = now
        if item in self._cache:
            c = self._cache[item]
            c['expiry'] = now + self._expire_time
            return c['data']
        else:
            obj = BytesIO()
            with open(item, 'rb') as f:
                obj.write(f.read())
            obj.seek(0)
            self._cache[item] = {'data': obj, 'expiry': now + self._expire_time}
            return obj

    def get(self, item):
        return self.__getitem__(item)

    def get_font(self, item, *args, **kwargs):
        now = time()
        cache_unique = "{}{}{}".format(hash(item), hash(args), hash(frozenset(kwargs.items())))
        if self._last_gc + self._gc_interval < now:
            self._gc_loop.call_soon_threadsafe(self._run_gc, self)
            self._last_gc = now
        if cache_unique in self._cache:
            c = self._cache[cache_unique]
            c['expiry'] = now + self._expire_time
            return c['data']
        else:
            obj = ImageFont.truetype(item, *args, **kwargs)
            self._cache[item] = {'data': obj, 'expiry': now + self._expire_time}
            return obj

    def __contains__(self, item):
        return item in self._cache

    def __setitem__(self, key, value):
        self._cache[key] = {
            'data': value,
            'expiry': time() + self._expire_time
        }

    def expired_on(self, item):
        return self._cache[item]['expiry']

    def set(self, key, value):
        return self.__setitem__(key, value)
