from io import BytesIO

from flask import send_file
from PIL import Image

from utils import http
from utils.endpoint import Endpoint


class Ugly(Endpoint):
    def generate(self, avatars, text, usernames):
        base = Image.open('assets/ugly/ugly.png').convert('RGBA')
        avatar = http.get_image(avatars[0]).resize((175, 175)).convert('RGBA')
        base.paste(avatar, (120, 55), avatar)

        b = BytesIO()
        base.save(b, format='png')
        b.seek(0)
        return send_file(b, mimetype='image/png')


def setup():
    return Ugly()
