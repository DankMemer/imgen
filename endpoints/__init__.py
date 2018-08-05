import sys

from . import (abandon, ban, bed, brain,  # noqa: F401
               byemom, disability, facts, gay, hitler, invert, jail,
               quote, shit, sickfilth, slap, spank, trash, trigger, tweet, ugly,
               warp, whodidthis, magik, deepfry, brazzers, cancer, cry, dab,
               delete, door, egg, failure, fakenews, fedora, floor, laid, note,
               ohno, plan, rip, satan, savehumanity, thesearch, dank)

endpoints = {}


for e in filter(lambda module: str(module).startswith('endpoints.'), sys.modules):
    endpoint = sys.modules[e].setup()
    endpoints.update({endpoint.name: endpoint})
