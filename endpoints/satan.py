from io import BytesIO

from PIL import Image
from flask import send_file

from utils import http
from utils.endpoint import Endpoint


class Satan(Endpoint):
    params = ['avatar0']

    def generate(self, avatars, text, usernames):
        base = Image.open(self.assets.get('assets/satan/satan.bmp')).convert('RGBA')
        avatar = http.get_image(avatars[0]).resize((195, 195)).convert('RGBA')
        final_image = Image.new('RGBA', base.size)

        # Put the base over the avatar
        final_image.paste(avatar, (200, 90), avatar)
        final_image.paste(base, (0, 0), base)
        final_image = final_image.convert('RGB')

        b = BytesIO()
        final_image.save(b, format='jpeg')
        b.seek(0)
        return send_file(b, mimetype='image/jpeg')


def setup(cache):
    return Satan(cache)
