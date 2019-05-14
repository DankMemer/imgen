from datetime import datetime
from io import BytesIO

from PIL import Image, ImageDraw, ImageOps
from flask import send_file

from utils import http
from utils.endpoint import Endpoint, setup
from utils.textutils import render_text_with_emoji


@setup
class Quote(Endpoint):
    params = ['avatar0', 'username0', 'text']

    def generate(self, avatars, text, usernames, kwargs):
        avatar = http.get_image(avatars[0]).resize((150, 150))
        base = Image.new('RGBA', (1500, 300))
        font_med = self.assets.get_font('assets/fonts/medium.woff', size=60)
        font_time = self.assets.get_font('assets/fonts/medium.woff', size=40)
        font_sb = self.assets.get_font('assets/fonts/semibold.woff', size=55)

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

        render_text_with_emoji(base, canvas, (230, 70), usernames[0], font=font_med, fill='White')
        render_text_with_emoji(base, canvas, (230, 150), text, font=font_sb, fill=(160, 160, 160))

        timestamp_left = 230 + canvas.textsize(usernames[0], font=font_med)[0] + 20
        render_text_with_emoji(base, canvas, (timestamp_left, 90), 'Today at {}'.format(datetime.utcnow().strftime("%H:%M")), font=font_time,
                    fill=(125, 125, 125))

        final = Image.alpha_composite(base, words)
        downscaled = final.resize((500, 100), Image.ANTIALIAS)
        downscaled = downscaled.convert('RGBA')

        b = BytesIO()
        downscaled.save(b, format='png')
        b.seek(0)
        return send_file(b, mimetype='image/png')
