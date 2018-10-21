from io import BytesIO

from PIL import Image
from flask import send_file

from utils import http
from utils.endpoint import Endpoint


class Egg(Endpoint):
    def generate(self, avatars, text, usernames):
        base = Image.open('assets/egg/egg.png').resize((350, 350)).convert('RGBA')
        avatar = http.get_image(avatars[0]).resize((50, 50)).convert('RGBA')

        base.paste(avatar, (143, 188), avatar)

        b = BytesIO()
        base.save(b, format='png')
        b.seek(0)
        return send_file(b, mimetype='image/png')


def setup():
    return Egg()
