from io import BytesIO

from PIL import Image, ImageDraw, ImageFont
from flask import send_file

from utils.endpoint import Endpoint
from utils.textutils import wrap


class TheSearch(Endpoint):
    def generate(self, avatars, text, usernames):
        base = Image.open('assets/search/thesearch.png').convert('RGBA')
        text_layer = Image.new('RGBA', base.size)
        font = ImageFont.truetype(font='assets/fonts/sans.ttf', size=16)
        canv = ImageDraw.Draw(text_layer)

        text = wrap(font, text, 178)
        canv.text((65, 335), text, font=font, fill='Black')

        base.paste(text_layer, (0, 0), text_layer)

        b = BytesIO()
        base.save(b, format='png')
        b.seek(0)
        return send_file(b, mimetype='image/png')


def setup():
    return TheSearch()
