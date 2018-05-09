from io import BytesIO

from flask import send_file
from PIL import Image

from utils import http
from utils.endpoint import Endpoint


class Disability(Endpoint):
    def generate(self, avatars, **kwargs):
        avatar = Image.open(http.get_image(avatars[0])).resize((175, 175))
        base = Image.open('assets/disability/disability.jpg')

        base.paste(avatar, (450, 325), avatar)

        b = BytesIO()
        base.save(b, format='png')
        b.seek(0)
        return send_file(b, mimetype='image/png')


def setup():
    return Disability()
