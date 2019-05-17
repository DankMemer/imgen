from io import BytesIO

from PIL import Image, ImageDraw
from flask import send_file

from utils.endpoint import Endpoint, setup
from utils.textutils import wrap, render_text_with_emoji


@setup
class Ohno(Endpoint):
    params = ['text']

    def generate(self, avatars, text, usernames, kwargs):
        base = Image.open(self.assets.get('assets/ohno/ohno.bmp')).convert('RGBA')
        font = self.assets.get_font('assets/fonts/sans.ttf', size=16 if len(text) > 38 else 32)
        canv = ImageDraw.Draw(base)

        text = wrap(font, text, 260)
        render_text_with_emoji(base, canv, (340, 30), text, font=font, fill='Black')
        base = base.convert('RGB')

        b = BytesIO()
        base.save(b, format='jpeg')
        b.seek(0)
        return send_file(b, mimetype='image/jpeg')
