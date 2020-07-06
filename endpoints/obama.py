from io import BytesIO

from PIL import Image, ImageDraw
from flask import send_file

from utils.endpoint import Endpoint, setup
from utils.textutils import render_text_with_emoji, wrap
from utils import http


@setup
class Obama(Endpoint):
    params = ['text']

    def generate(self, avatars, text, usernames, kwargs):
        base = Image.open(self.assets.get('assets/obama/obama.jpg'))
        font = self.assets.get_font('assets/fonts/arimobold.ttf', size=36)
        canv = ImageDraw.Draw(base)

        avatar = http.get_image(avatars[0]).resize((200, 200), Image.LANCZOS).convert('RGBA')

        w, _ = canv.textsize(wrap(font, usernames[0], 400), font)

        base.paste(avatar, (120, 73), avatar)
        base.paste(avatar, (365, 0), avatar)

        render_text_with_emoji(base, canv, (int(210 - (w/2)), 400), wrap(font, usernames[0], 400), font, 'white')
        render_text_with_emoji(base, canv, (int(470 - (w/2)), 300), wrap(font, usernames[0], 400), font, 'white')

        base = base.convert('RGB')
        b = BytesIO()
        base.save(b, format='jpeg')
        b.seek(0)
        return send_file(b, mimetype='image/jpeg')
