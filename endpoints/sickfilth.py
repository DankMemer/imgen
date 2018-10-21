from io import BytesIO

from flask import send_file
from PIL import Image

from utils import http
from utils.endpoint import Endpoint


class SickBan(Endpoint):
    def generate(self, avatars, text, usernames):
        base = Image.open('assets/ban/ban.png').convert('RGBA')
        avatar = http.get_image(avatars[0]).resize((400, 400)).convert('RGBA')
        base.paste(avatar, (70, 344), avatar)

        b = BytesIO()
        base.save(b, format='png')
        b.seek(0)
        return send_file(b, mimetype='image/png')


def setup():
    return SickBan()
