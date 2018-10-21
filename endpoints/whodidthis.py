from io import BytesIO

from flask import send_file
from PIL import Image

from utils import http
from utils.endpoint import Endpoint


class Whodidthis(Endpoint):
    def generate(self, avatars, text, usernames):
        base = Image.open('assets/whodidthis/whodidthis.png')
        avatar = http.get_image(avatars[0]).resize((720, 405)).convert('RGBA')
        base.paste(avatar, (0, 159), avatar)

        b = BytesIO()
        base.save(b, format='png')
        b.seek(0)
        return send_file(b, mimetype='image/png')


def setup():
    return Whodidthis()
