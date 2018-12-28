from io import BytesIO

from PIL import Image, ImageDraw
from flask import send_file

from utils.endpoint import Endpoint, setup
from utils.textutils import wrap


@setup
class SlapsRoof(Endpoint):
    params = ['text']

    def generate(self, avatars, text, usernames, kwargs):
        base = Image.open(self.assets.get('assets/slapsroof/slapsroof.bmp'))
        font = self.assets.get_font('assets/fonts/medium.woff', size=33)
        canv = ImageDraw.Draw(base)
        suffix = ' in it'
        text = wrap(font, text + suffix, 1150)
        canv.text((335, 31), text, font=font, fill='Black')

        base = base.convert('RGB')
        b = BytesIO()
        base.save(b, format='jpeg')
        b.seek(0)
        return send_file(b, mimetype='image/jpeg')
