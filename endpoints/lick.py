from io import BytesIO

from PIL import Image, ImageDraw
from flask import send_file

from utils.endpoint import Endpoint, setup
from utils.textutils import render_text_with_emoji, wrap


@setup
class Lick(Endpoint):
    params = ['text']

    def generate(self, avatars, text, usernames, kwargs):
        text = text.replace(', ', ',').split(',')
        if len(text) != 2:
            text = ['Dank Memer', 'People who do not split with a comma']
        base = Image.open(self.assets.get('assets/lick/lick.jpg'))
        font = self.assets.get_font('assets/fonts/verdana.ttf', size=24)
        canv = ImageDraw.Draw(base)
        render_text_with_emoji(base, canv, (80, 200), wrap(font, text[0], 220), font, 'white')
        render_text_with_emoji(base, canv, (290, 240), wrap(font, text[1], 320), font, 'white')

        base = base.convert('RGB')
        b = BytesIO()
        base.save(b, format='jpeg')
        b.seek(0)
        return send_file(b, mimetype='image/jpeg')
