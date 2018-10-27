from io import BytesIO

from flask import send_file
from PIL import Image

from utils.endpoint import Endpoint
from utils import http


class BongoCat(Endpoint):
    def generate(self, avatars, text, usernames):
        base = Image.open('assets/bongocat/bongocat.png').convert('RGBA')
        avatar = http.get_image(avatars[0]).resize((750, 750)).convert('RGBA')

        avatar.paste(base, (0, 0), base)

        b = BytesIO()
        avatar.save(b, format='png')
        b.seek(0)
        return send_file(b, mimetype='image/png')


def setup():
    return BongoCat()
