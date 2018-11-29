from io import BytesIO

from PIL import Image
from flask import send_file

from utils import http
from utils.endpoint import Endpoint


class Ugly(Endpoint):
    params = ['avatar0']

    def generate(self, avatars, text, usernames):
        base = Image.open(self.assets.get('assets/ugly/ugly.bmp')).convert('RGBA')
        avatar = http.get_image(avatars[0]).resize((175, 175)).convert('RGBA')
        base.paste(avatar, (120, 55), avatar)
        base = base.convert('RGB')

        b = BytesIO()
        base.save(b, format='jpeg')
        b.seek(0)
        return send_file(b, mimetype='image/jpeg')


def setup(cache):
    return Ugly(cache)
