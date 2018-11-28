from io import BytesIO

from flask import send_file

from utils import gm
from utils.endpoint import Endpoint


class RadialBlur(Endpoint):
    def generate(self, avatars, text, usernames):
        output = gm.radial_blur(avatars[0], 15, 'png')

        b = BytesIO(output)
        b.seek(0)
        return send_file(b, mimetype='image/png')


def setup(cache):
    return RadialBlur(cache)
