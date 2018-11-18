from io import BytesIO

from PIL import Image, ImageDraw
from flask import send_file

from utils.endpoint import Endpoint
from utils.textutils import wrap


class Cry(Endpoint):
    def generate(self, avatars, text, usernames):
        base = Image.open(self.assets.get('assets/cry/cry.bmp'))
        font = self.assets.get_font('assets/fonts/tahoma.ttf', size=20)
        canv = ImageDraw.Draw(base)

        text = wrap(font, text, 180)
        canv.text((382, 80), text, font=font, fill='Black')

        b = BytesIO()
        base.save(b, format='jpeg')
        b.seek(0)
        return send_file(b, mimetype='image/jpeg')


def setup(cache):
    return Cry(cache)
