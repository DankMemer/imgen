from io import BytesIO

from PIL import Image, ImageDraw, ImageFont
from flask import send_file

from utils.endpoint import Endpoint
from utils.textutils import wrap


class Plan(Endpoint):
    def generate(self, avatars, text, usernames):
        base = Image.open('assets/plan/plan.png').convert('RGBA')
        font = ImageFont.truetype(font='assets/fonts/sans.ttf', size=16)
        canv = ImageDraw.Draw(base)

        words = text.split(', ')

        if len(words) != 3:
            words = ['you need three items for this command',
                     'and each should be split by commas',
                     'Example: pls plan 1, 2, 3']

        words = [wrap(font, w, 120) for w in words]

        a, b, c = words

        canv.text((190, 60), a, font=font, fill='Black')
        canv.text((510, 60), b, font=font, fill='Black')
        canv.text((190, 280), c, font=font, fill='Black')
        canv.text((510, 280), c, font=font, fill='Black')

        b = BytesIO()
        base.save(b, format='png')
        b.seek(0)
        return send_file(b, mimetype='image/png')


def setup():
    return Plan()
