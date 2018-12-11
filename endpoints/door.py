from io import BytesIO

from PIL import Image
from flask import send_file

from utils import http
from utils.endpoint import Endpoint, setup


@setup
class Door(Endpoint):
    params = ['avatar0']

    def generate(self, avatars, text, usernames, kwargs):
        base = Image.open(self.assets.get('assets/door/door.bmp')).convert('RGBA')
        avatar = http.get_image(avatars[0]).resize((479, 479)).convert('RGBA')
        final_image = Image.new('RGBA', base.size)

        # Put the base over the avatar
        final_image.paste(avatar, (250, 0), avatar)
        final_image.paste(base, (0, 0), base)
        final_image = final_image.convert('RGBA')

        b = BytesIO()
        final_image.save(b, format='png')
        b.seek(0)
        return send_file(b, mimetype='image/png')
