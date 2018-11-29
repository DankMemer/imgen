import os

prohibit_load = ['__init__']

for endpoint in os.listdir('endpoints'):
    if endpoint[:-3] in prohibit_load or not endpoint.endswith('.py'):
        continue

    __import__('endpoints.' + endpoint[:-3], globals(), locals())
