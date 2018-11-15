from io import BytesIO

from PIL import Image, ImageDraw
from flask import send_file

from utils.endpoint import Endpoint
from utils.textutils import wrap


class Ohno(Endpoint):
    def generate(self, avatars, text, usernames):
        base = Image.open(self.assets.get('assets/ohno/ohno.bmp')).convert('RGBA')
        font = self.assets.get_font('assets/fonts/sans.ttf', size=16 if len(text) > 38 else 32)
        canv = ImageDraw.Draw(base)

        text = wrap(font, text, 260)
        canv.text((340, 30), text, font=font, fill='Black')
        base = base.convert('RGB')

        b = BytesIO()
        base.save(b, format='jpeg')
        b.seek(0)
        return send_file(b, mimetype='image/jpeg')


def setup(cache):
    return Ohno(cache)
