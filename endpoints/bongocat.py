from io import BytesIO

from flask import send_file
from PIL import Image

from utils.endpoint import Endpoint
from utils import http


class BongoCat(Endpoint):
    def generate(self, avatars, text, usernames):
        base = Image.open(self.assets.get('assets/bongocat/bongocat.bmp')).convert('RGBA')
        avatar = http.get_image(avatars[0]).resize((750, 750)).convert('RGBA')

        avatar.paste(base, (0, 0), base)
        avatar = avatar.convert('RGB')

        b = BytesIO()
        avatar.save(b, format='jpeg')
        b.seek(0)
        return send_file(b, mimetype='image/jpeg')


def setup(cache):
    return BongoCat(cache)
