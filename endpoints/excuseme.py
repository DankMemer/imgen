from io import BytesIO

from PIL import Image, ImageDraw
from flask import send_file

from utils.endpoint import Endpoint
from utils.textutils import wrap


class ExcuseMe(Endpoint):
    def generate(self, avatars, text, usernames):
        base = Image.open(self.assets.get('assets/excuseme/excuseme.bmp'))

        font = self.assets.get_font('assets/fonts/sans.ttf', size=40)
        canv = ImageDraw.Draw(base)
        text = wrap(font, text, 787)
        canv.text((20, 15), text, font=font, fill='Black')

        base = base.convert('RGB')

        b = BytesIO()
        base.save(b, format='jpeg')
        b.seek(0)
        return send_file(b, mimetype='image/jpeg')


def setup(cache):
    return ExcuseMe(cache)
