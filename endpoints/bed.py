from io import BytesIO

from flask import send_file
from PIL import Image

from utils import http
from utils.endpoint import Endpoint


class Bed(Endpoint):
    def generate(self, avatars, text, usernames):
        base = Image.open('assets/bed/bed.png').convert('RGBA')
        avatar = http.get_image(avatars[0]).resize((100, 100)).convert('RGBA')
        avatar2 = http.get_image(avatars[1]).resize((70, 70)).convert('RGBA')
        avatar_small = avatar.copy().resize((70, 70))
        base.paste(avatar, (25, 100), avatar)
        base.paste(avatar, (25, 300), avatar)
        base.paste(avatar_small, (53, 450), avatar_small)
        base.paste(avatar2, (53, 575), avatar2)

        b = BytesIO()
        base.save(b, format='png')
        b.seek(0)
        return send_file(b, mimetype='image/png')


def setup():
    return Bed()
