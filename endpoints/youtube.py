from io import BytesIO

from flask import send_file
from PIL import Image, ImageDraw, ImageFont

from utils import http
from utils.endpoint import Endpoint
from utils.textutils import wrap

from random import randint


class Youtube(Endpoint):
    def generate(self, avatars, text, usernames):
        avatar = http.get_image(avatars[0]).resize((52, 52)).convert('RGBA')
        name = usernames[0]
        base = Image.open('assets/youtube/youtube.png').convert('RGBA')
        font = ImageFont.truetype(font='assets/fonts/robotomedium.ttf', size=17, )
        font2 = ImageFont.truetype(font='assets/fonts/robotoregular.ttf', size=17, )
        font3 = ImageFont.truetype(font='assets/fonts/robotoregular.ttf', size=19, )

        bigsize = (avatar.size[0] * 3, avatar.size[1] * 3)
        mask = Image.new('L', bigsize, 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0) + bigsize, fill=255)
        mask = mask.resize(avatar.size, Image.ANTIALIAS)
        avatar.putalpha(mask)

        base.paste(avatar, (17, 33), avatar)
        canv = ImageDraw.Draw(base)
        op = wrap(font, name, 1150)
        size = canv.textsize(name, font=font)
        comment = wrap(font3, text, 550)
        num = randint(1, 59)
        plural = '' if num == 1 else 's'
        time = f'{num} minute{plural} ago'
        canv.text((92, 34), op, font=font, fill='Black')
        canv.text((100 + size[0], 34), time, font=font2, fill='Grey')
        canv.text((92, 59), comment, font=font3, fill='Black')

        b = BytesIO()
        base.save(b, format='png')
        b.seek(0)
        return send_file(b, mimetype='image/png')


def setup():
    return Youtube()
