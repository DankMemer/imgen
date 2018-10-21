from datetime import datetime
from io import BytesIO

from flask import send_file
from PIL import Image, ImageDraw, ImageFont, ImageOps

from utils import http
from utils.endpoint import Endpoint


class Quote(Endpoint):
    def generate(self, avatars, text, usernames):
        avatar = http.get_image(avatars[0]).resize((150, 150))
        base = Image.new('RGBA', (1500, 300))
        font_med = ImageFont.truetype(font='assets/fonts/medium.woff', size=60)
        font_time = ImageFont.truetype(font='assets/fonts/medium.woff', size=40)
        font_sb = ImageFont.truetype(font='assets/fonts/semibold.woff', size=55)

        poly = Image.new('RGBA', avatar.size)
        pdraw = ImageDraw.Draw(poly)
        pdraw.ellipse([(0, 0), *avatar.size], fill=(255, 255, 255, 255))
        if poly.mode == 'RGBA':
            r, g, b, a = poly.split()
            rgb_image = Image.merge('RGB', (r, g, b))
            inverted = ImageOps.invert(rgb_image)
            r, g, b = inverted.split()
            iv = Image.merge('RGBA', (r, g, b, a))
        else:
            iv = ImageOps.invert(poly)

        base.paste(avatar, (15, 75), mask=iv)

        words = Image.new('RGBA', base.size)
        canvas = ImageDraw.Draw(words)

        canvas.text((230, 70), usernames[0], font=font_med, fill='White')
        canvas.text((230, 150), text, font=font_sb, fill=(160, 160, 160))

        timestamp_left = 230 + canvas.textsize(usernames[0], font=font_med)[0] + 20
        canvas.text((timestamp_left, 90), 'Today at {}'.format(datetime.utcnow().strftime("%H:%M")), font=font_time, fill=(125, 125, 125))

        final = Image.alpha_composite(base, words)
        downscaled = final.resize((500, 100), Image.ANTIALIAS)

        b = BytesIO()
        downscaled.save(b, format='png')
        b.seek(0)
        return send_file(b, mimetype='image/png')


def setup():
    return Quote()
