from io import BytesIO

from flask import send_file
from PIL import Image

from utils import http
from utils.endpoint import Endpoint

from math import pi, cos, sin

class Affect(Endpoint):
    def generate(self, avatars, text, usernames):
        avatar = http.get_image(avatars[0]).resize((200, 157)).convert('RGBA')
        base = Image.open('assets/affect/affect.png').convert('RGBA')


        base.paste(avatar, (180, 383, 380, 540), avatar)

        b = BytesIO()
        base.save(b, format='png')
        b.seek(0)
        return send_file(b, mimetype='image/png')


def setup():
    return Affect()