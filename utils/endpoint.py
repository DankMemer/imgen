from abc import ABC, abstractmethod
from time import perf_counter

import rethinkdb as r

from utils.db import get_db, get_redis
from .asset_cache import AssetCache

asset_cache = AssetCache()
redis = get_redis()
endpoints = {}


class RedisFixedList:
    def __init__(self, key: str):
        self._keys = ("%s-usage" % key, "%s-times" % key)

    @property
    def hits(self):
        return int(redis.get(self._keys[0]) or 0)

    @property
    def list(self):
        return [float(x) for x in redis.lrange(self._keys[1], 0, 20)]

    def __len__(self):
        return redis.llen(self._keys[1])

    def __iter__(self):
        for x in redis.get(self._keys[1]) or []:
            yield float(x)

    def increment(self):
        redis.incr(self._keys[0])
        return self

    def append(self, value):
        redis.lpush(self._keys[1], value)
        redis.ltrim(self._keys[1], 0, 20)


class Endpoint(ABC):
    def __init__(self, cache):
        self.avg_generation_times = RedisFixedList(self.name)
        self.hits = self.avg_generation_times.hits
        self.assets = cache

    @property
    def name(self):
        return self.__class__.__name__.lower()

    def get_avg_gen_time(self):
        if len(self.avg_generation_times) == 0:
            return 0

        return round(sum(self.avg_generation_times.list) / len(self.avg_generation_times), 2)

    def run(self, key, **kwargs):
        self.avg_generation_times.increment()
        self.hits = self.avg_generation_times.hits
        start = perf_counter()
        res = self.generate(**kwargs)
        t = round((perf_counter() - start) * 1000, 2)  # Time in ms, formatted to 2dp
        self.avg_generation_times.append(t)
        k = r.table('keys').get(key).run(get_db())
        usage = k['usages'].get(self.name, 0) + 1
        r.table('keys').get(key) \
            .update({"total_usage": k['total_usage'] + 1,
                     "usages": {self.name: usage}}) \
            .run(get_db())
        return res

    @abstractmethod
    def generate(self, avatars, text, usernames):
        raise NotImplementedError(
            f"generate has not been implemented on endpoint {self.name}"
        )


def setup(klass):
    kls = klass(asset_cache)
    endpoints[kls.name] = kls
    return kls
