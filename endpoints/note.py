from io import BytesIO

from PIL import Image, ImageDraw, ImageFont
from flask import send_file

from utils.endpoint import Endpoint
from utils.textutils import wrap


class Note(Endpoint):
    def generate(self, avatars, text, usernames):
        base = Image.open('assets/note/note.png').convert('RGBA')
        text_layer = Image.new('RGBA', base.size)
        font = ImageFont.truetype(font='assets/fonts/sans.ttf', size=16)
        canv = ImageDraw.Draw(text_layer)

        text = wrap(font, text, 150)
        canv.text((455, 420), text, font=font, fill='Black')

        text_layer = text_layer.rotate(-23)

        base.paste(text_layer, (0, 0), text_layer)

        b = BytesIO()
        base.save(b, format='png')
        b.seek(0)
        return send_file(b, mimetype='image/png')


def setup():
    return Note()
