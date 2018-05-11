from io import BytesIO

from flask import send_file
from PIL import Image, ImageDraw, ImageFont

from utils.endpoint import Endpoint
from utils.textutils import wrap


class Tweet(Endpoint):
    def generate(self, avatars, text, usernames):
        base = Image.open('assets/tweet/trump.jpg')
        font = ImageFont.truetype(font='assets/fonts/segoeuireg.ttf', size=50)
        canv = ImageDraw.Draw(base)
        text = wrap(font, text, 1150)
        canv.text((45, 160), text, font=font, fill='Black')

        b = BytesIO()
        base.save(b, format='png')
        b.seek(0)
        return send_file(b, mimetype='image/png')


def setup():
    return Tweet()
