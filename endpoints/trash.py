from io import BytesIO

from flask import send_file
from PIL import Image, ImageFilter

from utils import http
from utils.endpoint import Endpoint


class Trash(Endpoint):
    def generate(self, avatars, text, usernames):
        avatar = http.get_image(avatars[0]).resize((483, 483)).convert('RGBA')
        base = Image.open('assets/trash/trash.png').convert('RGBA')

        avatar = avatar.filter(ImageFilter.GaussianBlur(radius=6))
        base.paste(avatar, (480, 0), avatar)

        b = BytesIO()
        base.save(b, format='png')
        b.seek(0)
        return send_file(b, mimetype='image/png')


def setup():
    return Trash()
