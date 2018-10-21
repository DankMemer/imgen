from io import BytesIO

from PIL import Image
from flask import send_file

from utils import http
from utils.endpoint import Endpoint


class Delete(Endpoint):
    def generate(self, avatars, text, usernames):
        base = Image.open('assets/delete/delete.png').convert('RGBA')
        avatar = http.get_image(avatars[0]).resize((195, 195)).convert('RGBA')

        base.paste(avatar, (120, 135), avatar)

        b = BytesIO()
        base.save(b, format='png')
        b.seek(0)
        return send_file(b, mimetype='image/png')


def setup():
    return Delete()
