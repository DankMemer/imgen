from io import BytesIO

from PIL import Image, ImageDraw
from flask import send_file

from utils import http
from utils.endpoint import Endpoint, setup
from utils.textutils import auto_text_size, render_text_with_emoji


@setup
class WhoThisIs(Endpoint):
    params = ['avatar0', 'text']

    def generate(self, avatars, text, usernames, kwargs):
        base = Image.open(self.assets.get('assets/whothisis/whothisis.bmp'))
        avatar = http.get_image(avatars[0]).resize((215, 215)).convert('RGBA')
        font = self.assets.get_font('assets/fonts/arimobold.ttf', size=40)
        base.paste(avatar, (523, 15), avatar)
        base.paste(avatar, (509, 567), avatar)
        base = base.convert('RGBA')

        canv = ImageDraw.Draw(base)
        render_text_with_emoji(base, canv, (545, 465), text, font=font, fill='White')

        b = BytesIO()
        base.save(b, format='png')
        b.seek(0)
        return send_file(b, mimetype='image/png')
