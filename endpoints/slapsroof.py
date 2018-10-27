from io import BytesIO

from flask import send_file
from PIL import Image, ImageDraw, ImageFont

from utils.endpoint import Endpoint
from utils.textutils import wrap


class SlapsRoof(Endpoint):
    def generate(self, avatars, text, usernames):
        base = Image.open('assets/slapsroof/slapsroof.png')
        font = ImageFont.truetype(font='assets/fonts/medium.woff', size=33)
        canv = ImageDraw.Draw(base)
        suffix = ' in it'
        text = wrap(font, text + suffix, 1150)
        canv.text((335, 31), text, font=font, fill='Black')

        b = BytesIO()
        base.save(b, format='png')
        b.seek(0)
        return send_file(b, mimetype='image/png')


def setup():
    return SlapsRoof()
