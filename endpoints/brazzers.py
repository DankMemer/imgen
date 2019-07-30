from io import BytesIO

from PIL import Image
from flask import send_file

from utils import http
from utils.endpoint import Endpoint, setup


@setup
class Brazzers(Endpoint):
    params = ['avatar0']

    def generate(self, avatars, text, usernames, kwargs):
        avatar = http.get_image(avatars[0]).convert('RGBA')
        base = Image.open(self.assets.get('assets/brazzers/brazzers.bmp'))
        aspect = avatar.width / avatar.height

        new_height = int(base.height * aspect)
        new_width = int(base.width * aspect)
        scale = new_width / avatar.width
        size = (int(new_width / scale / 2), int(new_height / scale / 2))

        base = base.resize(size).convert('RGBA')

        # avatar is technically the base
        avatar.paste(base, (avatar.width - base.width,
                            avatar.height - base.height), base)
        avatar = avatar.convert('RGBA')

        b = BytesIO()
        avatar.save(b, format='png')
        b.seek(0)
        return send_file(b, mimetype='image/png')
