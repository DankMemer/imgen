from io import BytesIO

from PIL import Image
from flask import send_file

from utils import http
from utils.endpoint import Endpoint


class Failure(Endpoint):
    def generate(self, avatars, text, usernames):
        base = Image.open('assets/failure/failure.jpg').convert('RGBA')
        avatar = http.get_image(avatars[0]).resize((215, 215)).convert('RGBA')

        base.paste(avatar, (143, 525), avatar)

        b = BytesIO()
        base.save(b, format='png')
        b.seek(0)
        return send_file(b, mimetype='image/png')


def setup():
    return Failure()
