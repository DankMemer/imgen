from io import BytesIO

from PIL import Image
from flask import send_file

from utils import http
from utils.endpoint import Endpoint, setup


@setup
class Brazzers(Endpoint):
    params = ['avatar0']

    def generate(self, avatars, text, usernames, kwargs):
        base = Image.open(self.assets.get('assets/brazzers/brazzers.bmp')).resize((300, 150)).convert('RGBA')
        avatar = http.get_image(avatars[0]).resize((500, 500)).convert('RGBA')

        # avatar is technically the base
        avatar.paste(base, (200, 390), base)
        avatar = avatar.convert('RGBA')

        b = BytesIO()
        avatar.save(b, format='png')
        b.seek(0)
        return send_file(b, mimetype='image/png')
