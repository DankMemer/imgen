from io import BytesIO

from PIL import Image, ImageDraw
from flask import send_file

from utils.endpoint import Endpoint, setup
from utils.textutils import wrap, render_text_with_emoji


@setup
class Walking(Endpoint):
    params = ['text']

    def generate(self, avatars, text, usernames, kwargs):
        base = Image.open(self.assets.get('assets/walking/walking.bmp'))

        font = self.assets.get_font('assets/fonts/sans.ttf', size=50)
        canv = ImageDraw.Draw(base)
        text = wrap(font, text, 1000)
        render_text_with_emoji(base, canv, (35, 35), text, font=font, fill='black')

        base = base.convert('RGB')

        b = BytesIO()
        base.save(b, format='jpeg')
        b.seek(0)
        return send_file(b, mimetype='image/jpeg')
