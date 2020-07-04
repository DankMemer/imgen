from io import BytesIO

from PIL import Image, ImageDraw
from flask import send_file

from utils.endpoint import Endpoint, setup
from utils.textutils import wrap


@setup
class ExpandingWWE(Endpoint):
    params = ['text']

    def generate(self, avatars, text, usernames, kwargs):
        base = Image.open(self.assets.get('assets/expandingwwe/expandingwwe.jpg'))
        font = self.assets.get_font('assets/fonts/verdana.ttf', size=30)

        text = text.replace(', ', ',')

        if len(text.split(',')) < 5:
            a, b, c, d, e = 'you need, five items, for this, command, (split by commas)'.split(',')
        else:
            a, b, c, d, e = text.split(',', 4)

        a, b, c, d, e = [wrap(font, i, 225).strip() for i in [a, b, c, d, e]]

        canvas = ImageDraw.Draw(base)
        canvas.text((5, 5), a, font=font, fill='Black')
        canvas.text((5, 205), b, font=font, fill='Black')
        canvas.text((5, 410), c, font=font, fill='Black')
        canvas.text((5, 620), d, font=font, fill='Black')
        canvas.text((5, 825), e, font=font, fill='Black')

        b = BytesIO()
        base.save(b, format='jpeg')
        b.seek(0)
        return send_file(b, mimetype='image/jpeg')
