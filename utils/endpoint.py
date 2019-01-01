from abc import ABC, abstractmethod
from time import perf_counter

import rethinkdb as r

from utils import fixedlist
from utils.db import get_db, get_redis
from .asset_cache import AssetCache
from utils.ratelimits import RatelimitCache

from datetime import timedelta

asset_cache = AssetCache()
endpoints = {}

buckets = {}


class Endpoint(ABC):
    def __init__(self, cache, rate, per):
        self.avg_generation_times = fixedlist.FixedList(name=self.name, maximum_item_count=20)
        self.assets = cache
        self.rate = rate
        self.per = per

    @property
    def name(self):
        return self.__class__.__name__.lower()

    @property
    def bucket(self):
        return buckets.get(self.name)

    def get_avg_gen_time(self):
        if self.avg_generation_times.len() == 0:
            return 0

        return round(self.avg_generation_times.sum(), 2)

    def run(self, key, **kwargs):
        get_redis().incr(self.name + ':hits')
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
    def generate(self, avatars, text, usernames, kwargs):
        raise NotImplementedError(
            f"generate has not been implemented on endpoint {self.name}"
        )


def setup(klass=None, rate=5, per=1):
    if klass:
        kls = klass(asset_cache, rate, per)
        endpoints[kls.name] = kls
        buckets[kls.name] = RatelimitCache(name=kls.name, expire_time=timedelta(0, per, 0))
        return kls
    else:
        def wrapper(klass, *a, **ka):
            kls = klass(asset_cache, rate, per)
            endpoints[kls.name] = kls
            buckets[kls.name] = RatelimitCache(name=kls.name, expire_time=timedelta(0, per, 0))
            return kls
        return wrapper
