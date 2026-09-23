from io import BytesIO

from PIL import Image, ImageDraw
from flask import send_file

from utils.endpoint import Endpoint, setup
from utils.textutils import wrap


@setup
class Brain(Endpoint):
    params = ['text1', 'text2', 'text3', 'text4']

    def generate(self, avatars, text, usernames, kwargs):
        base = Image.open(self.assets.get('assets/brain/brain.bmp'))
        font = self.assets.get_font('assets/fonts/verdana.ttf', size=30)

        a, b, c, d = self.text_fields(kwargs, 4)

        a, b, c, d = [wrap(font, i, 225).strip() for i in [a, b, c, d]]

        canvas = ImageDraw.Draw(base)
        canvas.text((15, 40), a, font=font, fill='Black')
        canvas.text((15, 230), b, font=font, fill='Black')
        canvas.text((15, 420), c, font=font, fill='Black')
        canvas.text((15, 610), d, font=font, fill='Black')

        b = BytesIO()
        base.save(b, format='jpeg')
        b.seek(0)
        return send_file(b, mimetype='image/jpeg')
