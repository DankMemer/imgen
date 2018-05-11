from io import BytesIO

from flask import send_file
from PIL import Image, ImageDraw, ImageFont

from utils.endpoint import Endpoint
from utils.textutils import wrap


class Brain(Endpoint):
    def generate(self, avatars, text, usernames):
        base = Image.open('assets/brain/brain.jpg')
        font = ImageFont.truetype('assets/fonts/verdana.ttf', size=30)

        if len(text.split(',')) < 4:
            a, b, c, d = 'you need, four items, for this, command (split by commas)'.split(',')
        else:
            a, b, c, d = text.split(',')

        a, b, c, d = [wrap(font, i, 225) for i in [a, b, c, d]]

        canvas = ImageDraw.Draw(base)
        canvas.text((15, 40), a.strip(), font=font, fill='Black')
        canvas.text((15, 230), b.strip(), font=font, fill='Black')
        canvas.text((15, 420), c.strip(), font=font, fill='Black')
        canvas.text((15, 610), d.strip(), font=font, fill='Black')

        b = BytesIO()
        base.save(b, format='png')
        b.seek(0)
        return send_file(b, mimetype='image/png')


def setup():
    return Brain()
