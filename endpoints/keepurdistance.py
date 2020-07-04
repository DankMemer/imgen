from io import BytesIO

from PIL import Image, ImageDraw
from flask import send_file

from utils.endpoint import Endpoint, setup
from utils.textutils import render_text_with_emoji, wrap


@setup
class KeepUrDistance(Endpoint):
    params = ['text']

    def generate(self, avatars, text, usernames, kwargs):
        base = Image.open(self.assets.get('assets/keepurdistance/keepurdistance.png'))
        font = self.assets.get_font('assets/fonts/MontserratBold.ttf', size=24)
        canv = ImageDraw.Draw(base)

        text = text.upper()

        if len(text) >= 30:
            text  = text[:27] + '...'
        render_text_with_emoji(base, canv, (92, 660), wrap(font, text, 440), font, 'white')

        base = base.convert('RGB')
        b = BytesIO()
        base.save(b, format='jpeg')
        b.seek(0)
        return send_file(b, mimetype='image/jpeg')
