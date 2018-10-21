from io import BytesIO

from flask import send_file
from PIL import Image

from utils import http
from utils.endpoint import Endpoint


class MadeThis(Endpoint):
    def generate(self, avatars, text, usernames):
        base = Image.open('assets/madethis/madethis.png').convert('RGBA')
        avatar = http.get_image(avatars[0]).resize((130, 130)).convert('RGBA')
        avatar2 = http.get_image(avatars[1]).resize((111, 111)).convert('RGBA')
        base.paste(avatar, (92, 271), avatar)
        base.paste(avatar2, (422, 267), avatar2)
        base.paste(avatar2, (406, 678), avatar2)
        base.paste(avatar2, (412, 1121), avatar2)

        b = BytesIO()
        base.save(b, format='png')
        b.seek(0)
        return send_file(b, mimetype='image/png')


def setup():
    return MadeThis()
