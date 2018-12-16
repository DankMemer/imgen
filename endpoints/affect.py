from io import BytesIO

from PIL import Image
from flask import send_file

from utils import http
from utils.endpoint import Endpoint, setup


@setup
class Affect(Endpoint):
    params = ['avatar0']

    def generate(self, avatars, text, usernames, kwargs):
        avatar = http.get_image(avatars[0]).resize((200, 157)).convert('RGBA')
        base = Image.open(self.assets.get('assets/affect/affect.bmp')).convert('RGBA')

        base.paste(avatar, (180, 383, 380, 540), avatar)
        base = base.convert('RGB')

        b = BytesIO()
        base.save(b, format='jpeg')
        b.seek(0)
        return send_file(b, mimetype='image/jpeg')
