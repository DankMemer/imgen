from io import BytesIO

from PIL import Image, ImageDraw
from flask import send_file

from utils.endpoint import Endpoint, setup
from utils.textutils import render_text_with_emoji, wrap


@setup
class GodWhy(Endpoint):
    params = ['text']

    def generate(self, avatars, text, usernames, kwargs):
        base = Image.open(self.assets.get('assets/godwhy/godwhy.png')).resize((1061, 1080), Image.LANCZOS)
        font = self.assets.get_font('assets/fonts/verdana.ttf', size=24)
        canv = ImageDraw.Draw(base)

        if len(text) >= 127:
            text = text[:124] + '...'
        
        render_text_with_emoji(base, canv, (35, 560), wrap(font, text, 370), font, 'black')

        base = base.convert('RGB')
        b = BytesIO()
        base.save(b, format='jpeg')
        b.seek(0)
        return send_file(b, mimetype='image/jpeg')
