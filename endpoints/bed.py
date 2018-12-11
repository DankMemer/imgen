from io import BytesIO

from PIL import Image
from flask import send_file

from utils import http
from utils.endpoint import Endpoint, setup


@setup
class Bed(Endpoint):
    params = ['avatar0', 'avatar1']

    def generate(self, avatars, text, usernames, kwargs):
        base = Image.open(self.assets.get('assets/bed/bed.bmp')).convert('RGBA')
        avatar = http.get_image(avatars[0]).resize((100, 100)).convert('RGBA')
        avatar2 = http.get_image(avatars[1]).resize((70, 70)).convert('RGBA')
        avatar_small = avatar.copy().resize((70, 70))
        base.paste(avatar, (25, 100), avatar)
        base.paste(avatar, (25, 300), avatar)
        base.paste(avatar_small, (53, 450), avatar_small)
        base.paste(avatar2, (53, 575), avatar2)
        base = base.convert('RGBA')

        b = BytesIO()
        base.save(b, format='png')
        b.seek(0)
        return send_file(b, mimetype='image/png')
