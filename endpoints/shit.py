from io import BytesIO

from flask import send_file
from PIL import Image, ImageDraw, ImageFont

from utils.endpoint import Endpoint
from utils.textutils import wrap


class Shit(Endpoint):
    def generate(self, avatars, text, usernames):
        base = Image.open('assets/shit/shit.jpg')
        font = ImageFont.truetype(font='assets/fonts/segoeuireg.ttf', size=30)

        text_layer = Image.new('RGBA', base.size)
        canv = ImageDraw.Draw(text_layer)

        text = wrap(font, text, 350)
        canv.text((0, 570), text, font=font, fill='Black')
        text_layer = text_layer.rotate(52, resample=Image.BICUBIC)

        base.paste(text_layer, (0, 50), text_layer)

        b = BytesIO()
        base.save(b, format='png')
        b.seek(0)
        return send_file(b, mimetype='image/png')


def setup():
    return Shit()
