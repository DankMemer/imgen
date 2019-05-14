from io import BytesIO
from random import randint

from PIL import Image, ImageDraw
from flask import send_file

from utils import http
from utils.endpoint import Endpoint, setup
from utils.textutils import wrap, render_text_with_emoji


@setup
class Youtube(Endpoint):
    params = ['avatar0', 'username0', 'text']

    def generate(self, avatars, text, usernames, kwargs):
        avatar = http.get_image(avatars[0]).resize((52, 52)).convert('RGBA')
        name = usernames[0]
        base = Image.open(self.assets.get('assets/youtube/youtube.bmp')).convert('RGBA')
        font = self.assets.get_font('assets/fonts/robotomedium.ttf', size=17, )
        font2 = self.assets.get_font('assets/fonts/robotoregular.ttf', size=17, )
        font3 = self.assets.get_font('assets/fonts/robotoregular.ttf', size=19, )

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
        render_text_with_emoji(base, canv, (92, 34), op, font=font, fill='Black')
        render_text_with_emoji(base, canv, (100 + size[0], 34), time, font=font2, fill='Grey')
        render_text_with_emoji(base, canv, (92, 59), comment, font=font3, fill='Black')
        base = base.convert('RGBA')

        b = BytesIO()
        base.save(b, format='png')
        b.seek(0)
        return send_file(b, mimetype='image/png')
