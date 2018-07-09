from io import BytesIO

from flask import send_file
from PIL import Image, ImageDraw, ImageFont

from utils.endpoint import Endpoint
from utils.textutils import wrap


class Facts(Endpoint):
    def generate(self, avatars, text, usernames):
        base = Image.open('assets/facts/facts.jpg')
        # We need to create an image layer here for the rotation
        text_layer = Image.new('RGBA', base.size)
        font = ImageFont.truetype(font='assets/fonts/verdana.ttf', size=25)
        canv = ImageDraw.Draw(text_layer)

        text = wrap(font, text, 400)
        canv.text((90, 600), text, font=font, fill='Black')
        text_layer = text_layer.rotate(-13, resample=Image.BICUBIC)
        base.paste(text_layer, (0, 0), text_layer)

        b = BytesIO()
        base.save(b, format='png')
        b.seek(0)
        return send_file(b, mimetype='image/png')


def setup():
    return Facts()
