from io import BytesIO

from PIL import Image
from flask import send_file

from utils import http
from utils.endpoint import Endpoint


class Cancer(Endpoint):
    def generate(self, avatars, text, usernames):
        base = Image.open('assets/cancer/cancer.png').convert('RGBA')
        avatar = http.get_image(avatars[0]).resize((100, 100)).convert('RGBA')

        base.paste(avatar, (351, 200), avatar)

        b = BytesIO()
        base.save(b, format='png')
        b.seek(0)
        return send_file(b, mimetype='image/png')


def setup():
    return Cancer()
