from io import BytesIO

from flask import send_file
from PIL import Image

from utils import http
from utils.endpoint import Endpoint


class Roblox(Endpoint):
    def generate(self, avatars, text, usernames):
        base = Image.open('assets/roblox/roblox.png').convert('RGBA')
        avatar = http.get_image(avatars[0]).resize((56, 74)).convert('RGBA')
        base.paste(avatar, (168, 41), avatar)

        b = BytesIO()
        base.save(b, format='png')
        b.seek(0)
        return send_file(b, mimetype='image/png')


def setup():
    return Roblox()
