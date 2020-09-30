from io import BytesIO

from PIL import Image, ImageDraw
from flask import send_file

from utils.endpoint import Endpoint, setup
from utils.textutils import render_text_with_emoji, wrap


@setup
class TheOffice(Endpoint):
    params = ['text']

    def generate(self, avatars, text, usernames, kwargs):
        base = Image.open(self.assets.get('assets/theoffice/theoffice.png'))
        font = self.assets.get_font('assets/fonts/verdana.ttf', size=28)
        canv = ImageDraw.Draw(base)

        left, right = text.replace(', ', ',').split(',', 2)

        render_text_with_emoji(base, canv, (125, 200), wrap(font, left, 200), font, 'white')
        render_text_with_emoji(base, canv, (420, 250), wrap(font, right, 200), font, 'white')

        base = base.convert('RGB')
        b = BytesIO()
        base.save(b, format='jpeg')
        b.seek(0)
        return send_file(b, mimetype='image/jpeg')
