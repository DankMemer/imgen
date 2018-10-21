from io import BytesIO

from PIL import Image
from flask import send_file

from utils import http
from utils.endpoint import Endpoint


class Rip(Endpoint):
    def generate(self, avatars, text, usernames):
        base = Image.open('assets/rip/rip.png').convert('RGBA').resize((642, 806))
        avatar = http.get_image(avatars[0]).resize((300, 300)).convert('RGBA')

        base.paste(avatar, (175, 385), avatar)

        b = BytesIO()
        base.save(b, format='png')
        b.seek(0)
        return send_file(b, mimetype='image/png')


def setup():
    return Rip()
