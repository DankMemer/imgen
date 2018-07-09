from io import BytesIO

from PIL import Image, ImageDraw, ImageFont
from flask import send_file

from utils import http
from utils.endpoint import Endpoint
from utils.textutils import wrap


class Floor(Endpoint):
    def generate(self, avatars, text, usernames):
        base = Image.open('assets/floor/floor.jpg').convert('RGBA')
        # Open it twice because python
        avatar = Image.open(http.get_image(avatars[0])).resize((45, 45)).convert('RGBA')
        avatar2 = Image.open(http.get_image(avatars[0])).resize((23, 23)).convert('RGBA')
        text_layer = Image.new('RGBA', base.size)
        font = ImageFont.truetype(font='assets/fonts/sans.ttf', size=22)
        canv = ImageDraw.Draw(text_layer)

        text = wrap(font, text, 300)
        canv.text((168, 36), text, font=font, fill='Black')

        base.paste(avatar, (100, 90), avatar)
        base.paste(avatar2, (330, 90), avatar2)
        base.paste(text_layer, (0, 0), text_layer)

        b = BytesIO()
        base.save(b, format='png')
        b.seek(0)
        return send_file(b, mimetype='image/png')


def setup():
    return Floor()
