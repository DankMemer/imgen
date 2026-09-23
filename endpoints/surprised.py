from io import BytesIO

from PIL import Image, ImageDraw
from flask import send_file

from utils.endpoint import Endpoint, setup
from utils.textutils import wrap, render_text_with_emoji


@setup
class Surprised(Endpoint):
    params = ['text1', 'text2']

    def generate(self, avatars, text, usernames, kwargs):
        base = Image.open(self.assets.get('assets/surprised/surprised.bmp')).convert('RGBA')
        font = self.assets.get_font('assets/fonts/robotoregular.ttf', size=36)
        text1, text2 = self.text_fields(kwargs, 2)
        text1 = wrap(font, 'me: ' + text1, 650)
        text2 = wrap(font, 'also me: ' + text2, 650)
        canv = ImageDraw.Draw(base)
        render_text_with_emoji(base, canv, (20, 20), text1, font=font, fill='White')
        render_text_with_emoji(base, canv, (20, 140), text2, font=font, fill='White')
        base = base.convert('RGB')

        b = BytesIO()
        base.save(b, format='jpeg')
        b.seek(0)
        return send_file(b, mimetype='image/jpeg')
