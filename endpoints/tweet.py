from datetime import datetime
from io import BytesIO
from random import randint

from flask import send_file
from PIL import Image, ImageDraw

from utils import http
from utils.endpoint import Endpoint, setup
from utils.textutils import wrap, render_text_with_emoji


@setup
class Tweet(Endpoint):
    """
    Note: You can actually use username2 as a way to set the @handle separately from the name
    """
    params = ['avatar0', 'username0', 'text', 'username1', 'altstyle']

    def generate(self, avatars, text, usernames, kwargs):
        base = Image.open(self.assets.get('assets/tweet/trump.bmp'))
        avatar = http.get_image(avatars[0]).resize((98, 98)).convert('RGBA')
        font = self.assets.get_font('assets/fonts/segoeuireg.ttf', size=50, )
        font2 = self.assets.get_font('assets/fonts/robotomedium.ttf', size=40)
        font3 = self.assets.get_font('assets/fonts/robotoregular.ttf', size=29)
        font4 = self.assets.get_font('assets/fonts/robotoregular.ttf', size=35)

        circle = Image.new('L', (20, 20), 0)
        draw = ImageDraw.Draw(circle)
        draw.ellipse((0, 0, 20, 20), fill=255)
        alpha = Image.new('L', avatar.size, 255)
        w, h = avatar.size
        alpha.paste(circle.crop((0, 0, 10, 10)), (0, 0))
        alpha.paste(circle.crop((0, 10, 10, 10 * 2)), (0, h - 10))
        alpha.paste(circle.crop((10, 0, 10 * 2, 10)), (w - 10, 0))
        alpha.paste(circle.crop((10, 10, 10 * 2, 10 * 2)), (w - 10, h - 10))
        avatar.putalpha(alpha)

        base.paste(avatar, (42, 38), avatar)
        canv = ImageDraw.Draw(base)
        text2 = wrap(font2, usernames[0], 1150)
        tag_raw = usernames[1] if len(usernames) == 2 else usernames[0]
        text3 = wrap(font3, f'@{tag_raw}', 1150)

        time = datetime.now().strftime('%-I:%M %p - %d %b %Y')
        retweets = "{:,}".format(randint(0, 99999))
        likes = "{:,}".format(randint(0, 99999))
        text4 = wrap(font3, time, 1150)
        text5 = wrap(font4, retweets, 1150)
        text6 = wrap(font4, likes, 1150)
        total_size = (45, 160)
        for i in text.split(' '):
            i += ' '
            if i.startswith(('@', '#')):
                if total_size[0] > 1000:
                    total_size = (45, total_size[1] + 65)
                render_text_with_emoji(base, canv, total_size, i, font=font, fill='#1b95e0')
                y = canv.textsize(i, font=font)
                total_size = (total_size[0] + y[0], total_size[1])
            else:
                if total_size[0] > 1000:
                    total_size = (45, total_size[1] + 65)
                render_text_with_emoji(base, canv, total_size, i, font=font, fill='Black')
                y = canv.textsize(i, font=font)
                total_size = (total_size[0] + y[0], total_size[1])
        render_text_with_emoji(base, canv, (160, 45), text2, font=font2, fill='Black')
        render_text_with_emoji(base, canv, (160, 95), text3, font=font3, fill='Grey')
        render_text_with_emoji(base, canv, (40, 570), text4, font=font3, fill='Grey')
        render_text_with_emoji(base, canv, (40, 486), text5, font=font4, fill='#2C5F63')
        render_text_with_emoji(base, canv, (205, 486), text6, font=font4, fill='#2C5F63')

        b = BytesIO()
        base.save(b, format='png')
        b.seek(0)
        return send_file(b, mimetype='image/png')
