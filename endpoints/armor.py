from io import BytesIO

from PIL import Image, ImageDraw, ImageFont
from flask import send_file

from utils.endpoint import Endpoint
from utils.textutils import auto_text_size


class Armor(Endpoint):
    def generate(self, avatars, text, usernames):
        base = Image.open('assets/armor/armor.png').convert('RGBA')
        # We need a text layer here for the rotation
        font, text = auto_text_size(text, ImageFont.truetype(font='assets/fonts/sans.ttf'), 207, font_scalar=0.8)
        canv = ImageDraw.Draw(base)

        canv.text((34, 371), text, font=font, fill='Black')

        b = BytesIO()
        base.save(b, format='png')
        b.seek(0)
        return send_file(b, mimetype='image/png')


def setup():
    return Armor()
