from io import BytesIO

from PIL import Image, ImageDraw
from flask import send_file

from utils.endpoint import Endpoint, setup
from utils.textutils import wrap


@setup
class TheSearch(Endpoint):
    params = ['text']

    def generate(self, avatars, text, usernames, kwargs):
        base = Image.open(self.assets.get('assets/search/thesearch.bmp')).convert('RGBA')
        font = self.assets.get_font('assets/fonts/sans.ttf', size=16)
        canv = ImageDraw.Draw(base)

        text = wrap(font, text, 178)
        canv.text((65, 335), text, font=font, fill='Black')
        base = base.convert('RGB')

        b = BytesIO()
        base.save(b, format='jpeg')
        b.seek(0)
        return send_file(b, mimetype='image/jpeg')
