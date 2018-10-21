from io import BytesIO

from PIL import Image, ImageDraw, ImageFont
from flask import send_file

from utils.endpoint import Endpoint
from utils.textutils import auto_text_size


class KnowYourLocation(Endpoint):
    def generate(self, avatars, text, usernames):
        base = Image.open('assets/knowyourlocation/knowyourlocation.jpg').convert('RGBA')
        # We need a text layer here for the rotation
        canv = ImageDraw.Draw(base)

        text = text.split(', ')

        if len(text) != 2:
            text = ["Separate the items with a", "comma followed by a space"]

        top, bottom = text

        top_font, top_text = auto_text_size(top, ImageFont.truetype(font='assets/fonts/sans.ttf'), 630)
        bottom_font, bottom_text = auto_text_size(bottom, ImageFont.truetype(font='assets/fonts/sans.ttf'), 539)

        canv.text((64, 131), top_text, font=top_font, fill='Black')
        canv.text((120, 450), bottom_text, font=bottom_font, fill='Black')

        b = BytesIO()
        base.save(b, format='png')
        b.seek(0)
        return send_file(b, mimetype='image/png')


def setup():
    return KnowYourLocation()
