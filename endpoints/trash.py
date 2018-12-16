from io import BytesIO

from PIL import Image, ImageFilter
from flask import send_file

from utils import http
from utils.endpoint import Endpoint, setup


@setup
class Trash(Endpoint):
    params = ['avatar0']

    def generate(self, avatars, text, usernames, kwargs):
        avatar = http.get_image(avatars[0]).resize((483, 483)).convert('RGBA')
        base = Image.open(self.assets.get('assets/trash/trash.bmp')).convert('RGBA')

        avatar = avatar.filter(ImageFilter.GaussianBlur(radius=6))
        base.paste(avatar, (480, 0), avatar)
        base = base.convert('RGBA')

        b = BytesIO()
        base.save(b, format='png')
        b.seek(0)
        return send_file(b, mimetype='image/png')
