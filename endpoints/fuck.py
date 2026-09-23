from io import BytesIO

from PIL import Image, ImageDraw
from flask import send_file

from utils.endpoint import Endpoint, setup
from utils.textutils import render_text_with_emoji, wrap


@setup
class Fuck(Endpoint):
    params = ['text1', 'text2']

    def generate(self, avatars, text, usernames, kwargs):
        text = self.text_fields(kwargs, 2)
        base = Image.open(self.assets.get('assets/fuck/fuck.jpg'))
        font = self.assets.get_font('assets/fonts/verdana.ttf', size=24)
        canv = ImageDraw.Draw(base)
        render_text_with_emoji(base, canv, (200, 600), wrap(font, text[0], 320), font, 'white')
        render_text_with_emoji(base, canv, (750, 700), wrap(font, text[1], 320), font, 'white')

        base = base.convert('RGB')
        b = BytesIO()
        base.save(b, format='jpeg')
        b.seek(0)
        return send_file(b, mimetype='image/jpeg')
