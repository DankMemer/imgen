import sys

from .import (abandon, bed, brain,  # noqa: F401
              byemom, disability, facts, gay, hitler, invert, jail,
              quote, shit, sickfilth, slap, spank, trash, trigger, tweet, ugly,
              warp, whodidthis, magik, deepfry, brazzers)

endpoints = {}


for e in filter(lambda module: str(module).startswith('endpoints.'), sys.modules):
    endpoint = sys.modules[e].setup()
    endpoints.update({endpoint.name: endpoint})
