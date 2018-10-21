from io import BytesIO

from flask import send_file
from PIL import Image

from utils import http
from utils.endpoint import Endpoint


class Screams(Endpoint):
    def generate(self, avatars, text, usernames):
        base = Image.open('assets/screams/screams.jpg').convert('RGBA')
        avatar = http.get_image(avatars[0]).resize((175, 175)).convert('RGBA')
        avatar2 = http.get_image(avatars[1]).resize((156, 156)).convert('RGBA')
        base.paste(avatar, (200, 1), avatar)
        base.paste(avatar2, (136, 231), avatar2)

        b = BytesIO()
        base.save(b, format='png')
        b.seek(0)
        return send_file(b, mimetype='image/png')


def setup():
    return Screams()
