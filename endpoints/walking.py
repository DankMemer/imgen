from io import BytesIO

from PIL import Image, ImageDraw
from flask import send_file

from utils.endpoint import Endpoint
from utils.textutils import wrap


class Walking(Endpoint):
    def generate(self, avatars, text, usernames):
        base = Image.open(self.assets.get('assets/walking/walking.bmp'))

        font = self.assets.get_font('assets/fonts/sans.ttf', size=50)
        canv = ImageDraw.Draw(base)
        text = wrap(font, text, 1000)
        canv.text((35, 35), text, font=font, fill='Black')

        base = base.convert('RGB')

        b = BytesIO()
        base.save(b, format='jpeg')
        b.seek(0)
        return send_file(b, mimetype='image/jpeg')


def setup(cache):
    return Walking(cache)
