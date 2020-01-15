from io import BytesIO

from PIL import Image, ImageDraw
from flask import send_file

from utils.endpoint import Endpoint, setup
from utils.textutils import wrap, render_text_with_emoji


@setup
class DogLemon(Endpoint):
    params = ['text']

    def generate(self, avatars, text, usernames, kwargs):
        base = Image.open(self.assets.get('assets/doglemon/doglemon.bmp'))
        font = self.assets.get_font('assets/fonts/medium.woff', size=30)
        canv = ImageDraw.Draw(base)
        lemon, dog = text.replace(' ,', ',', 1).split(',', 1)
        lemon = wrap(font, lemon, 500)
        dog = wrap(font, dog, 450)
        render_text_with_emoji(base, canv, (750, 150), lemon[:180], font=font, fill='Black')
        render_text_with_emoji(base, canv, (33, 5), dog[:200], font=font, fill='White')

        base = base.convert('RGB')
        b = BytesIO()
        base.save(b, format='jpeg')
        b.seek(0)
        return send_file(b, mimetype='image/jpeg')
