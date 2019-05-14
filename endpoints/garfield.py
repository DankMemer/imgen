from io import BytesIO

from PIL import Image, ImageDraw
from flask import send_file

from utils.http import get_image

from utils.endpoint import Endpoint, setup
from utils.textutils import wrap, render_text_with_emoji


@setup
class Garfield(Endpoint):
    params = ['text', 'avatar0']

    def generate(self, avatars, text, usernames, kwargs):

        base = Image.open(self.assets.get('assets/garfield/garfield.png')).convert('RGB')
        no_entry = Image.open(self.assets.get('assets/garfield/no_entry.png')).convert('RGBA').resize((224, 224), Image.LANCZOS)
        font = self.assets.get_font('assets/fonts/arial.ttf', size=28)
        avatar = get_image(avatars[0]).resize((192, 192), Image.LANCZOS).convert('RGBA')
        avatar2 = avatar.copy().resize((212, 212), Image.LANCZOS).convert('RGBA')

        base.paste(avatar, (296, 219), avatar)
        base.paste(no_entry, (280, 203), no_entry)
        base.paste(avatar2, (40, 210), avatar2)

        draw = ImageDraw.Draw(base)
        render_text_with_emoji(base, draw, (15, 0), wrap(font, text, base.width), font, 'black')

        b = BytesIO()
        base.save(b, format='png')
        b.seek(0)
        return send_file(b, mimetype='image/png')
