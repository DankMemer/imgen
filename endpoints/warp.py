from io import BytesIO
from random import choice, randint

from flask import send_file

from utils import gm
from utils.endpoint import Endpoint


class Warp(Endpoint):
    def generate(self, avatars, text, usernames):
        implode = f'-{str(randint(3, 15))}'
        roll = f'+{randint(0, 256)}+{randint(0, 256)}'
        swirl = f'{choice(["+", "-"])}{randint(120, 180)}'
        concat = ['-implode', implode, '-roll', roll, '-swirl', swirl]

        output = gm.convert(avatars[0], concat, 'png')

        b = BytesIO(output)
        b.seek(0)
        return send_file(b, mimetype='image/png')


def setup():
    return Warp()
