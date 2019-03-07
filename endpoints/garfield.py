from io import BytesIO

from PIL import Image, ImageDraw
from flask import send_file

from utils.http import get_image

from utils.endpoint import Endpoint, setup
from utils.textutils import wrap


@setup
class Garfield(Endpoint):
    params = ['text', 'avatar0', 'avatar1']

    def generate(self, avatars, text, usernames, kwargs):
        base = Image.open(self.assets.get('assets/garfield/garfield.png')).convert('RGB')
        no_entry = Image.open(self.assets.get('assets/garfield/no_entry.png')).convert('RGBA').resize((224, 224), Image.LANCZOS)
        font = self.assets.get_font('assets/fonts/arial.ttf', size=28)
        avatar = get_image(avatars[0]).resize((192, 192), Image.LANCZOS)
        try:
            avatar2 = get_image(avatars[1]).resize((212, 212), Image.LANCZOS)
        except IndexError:
            avatar2 = get_image(avatars[0]).resize((212, 212), Image.LANCZOS)

        base.paste(avatar, (296, 219))
        base.paste(no_entry, (280, 203), no_entry)
        base.paste(avatar2, (40, 210))

        draw = ImageDraw.Draw(base)
        draw.text((15, 0), wrap(font, text, 565), font=font, fill='black')

        b = BytesIO()
        base.save(b, format='jpeg')
        b.seek(0)
        return send_file(b, mimetype='image/jpeg')
