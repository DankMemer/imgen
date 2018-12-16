from io import BytesIO
from random import choice, randint

from flask import send_file

from utils import gm
from utils.endpoint import Endpoint, setup


@setup
class Warp(Endpoint):
    params = ['avatar0']

    def generate(self, avatars, text, usernames, kwargs):
        implode = '-{}'.format(str(randint(3, 15)))
        roll = '+{}+{}'.format(randint(0, 256), randint(0, 256))
        swirl = '{}{}'.format(choice(["+", "-"]), randint(120, 180))
        concat = ['-implode', implode, '-roll', roll, '-swirl', swirl]

        output = gm.convert(avatars[0], concat, 'png')

        b = BytesIO(output)
        b.seek(0)
        return send_file(b, mimetype='image/png')
