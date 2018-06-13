import sys

from .import (abandon, ban, bed, brain,  # noqa: F401
              byemom, disability, facts, gay, hitler, invert, jail,
              quote, shit, slap, spank, trash, trigger, tweet, ugly,
              warp, whodidthis, magik, deepfry)

endpoints = {}


for e in filter(lambda module: str(module).startswith('endpoints.'), sys.modules):
    try:
        endpoint = sys.modules[e].setup()
        endpoints.update({endpoint.name: endpoint})
    except Exception:
        print('Failed to load ' + endpoint)
