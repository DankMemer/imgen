from abc import ABC, abstractmethod
from time import perf_counter

import rethinkdb as r

from utils import fixedlist
from utils.db import get_db
from .asset_cache import AssetCache

asset_cache = AssetCache()
endpoints = {}


class Endpoint(ABC):
    def __init__(self, cache):
        self.avg_generation_times = fixedlist.FixedList(20)
        self.hits = 0
        self.assets = cache

    @property
    def name(self):
        return self.__class__.__name__.lower()

    def get_avg_gen_time(self):
        if len(self.avg_generation_times) == 0:
            return 0

        return round(sum(self.avg_generation_times) / len(self.avg_generation_times), 2)

    def run(self, key, **kwargs):
        self.hits += 1
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
