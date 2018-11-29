from io import BytesIO

from PIL import Image
from flask import send_file

from utils import http
from utils.endpoint import Endpoint


class Disability(Endpoint):
    params = ['avatar0']

    def generate(self, avatars, text, usernames):
        avatar = http.get_image(avatars[0]).resize((175, 175)).convert('RGBA')
        base = Image.open(self.assets.get('assets/disability/disability.bmp')).convert('RGBA')

        base.paste(avatar, (450, 325), avatar)
        base = base.convert('RGB')

        b = BytesIO()
        base.save(b, format='jpeg')
        b.seek(0)
        return send_file(b, mimetype='image/jpeg')


def setup(cache):
    return Disability(cache)
