from io import BytesIO

from PIL import Image, ImageDraw, ImageFont
from flask import send_file

from utils.endpoint import Endpoint
from utils.textutils import auto_text_size


class ChangeMyMind(Endpoint):
    def generate(self, avatars, text, usernames):
        base = Image.open('assets/changemymind/changemymind.jpg').convert('RGBA')
        # We need a text layer here for the rotation
        text_layer = Image.new('RGBA', base.size)
        font, text = auto_text_size(text, ImageFont.truetype(font='assets/fonts/sans.ttf'), 310)
        canv = ImageDraw.Draw(text_layer)

        canv.text((290, 300), text, font=font, fill='Black')

        text_layer = text_layer.rotate(23, resample=Image.BICUBIC)

        base.paste(text_layer, (0, 0), text_layer)

        b = BytesIO()
        base.save(b, format='png')
        b.seek(0)
        return send_file(b, mimetype='image/png')


def setup():
    return ChangeMyMind()
