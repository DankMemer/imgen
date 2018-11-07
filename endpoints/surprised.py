from io import BytesIO

from PIL import Image, ImageDraw, ImageFont
from flask import send_file

from utils.endpoint import Endpoint
from utils.textutils import wrap


class Surprised(Endpoint):
    def generate(self, avatars, text, usernames):
        base = Image.open('assets/surprised/surprised.png').convert('RGBA')
        font = ImageFont.truetype(font='assets/fonts/robotoregular.ttf', size=36)
        text = wrap(font, 'me: ' + text, 650)
        canv = ImageDraw.Draw(base)
        canv.text((20, 20), text, font=font, fill='White')

        b = BytesIO()
        base.save(b, format='png')
        b.seek(0)
        return send_file(b, mimetype='image/png')


def setup():
    return Surprised()