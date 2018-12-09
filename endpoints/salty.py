from io import BytesIO
from random import randint

from PIL import Image
from flask import send_file

from utils import http
from utils.endpoint import Endpoint, setup


@setup
class Salty(Endpoint):
    params = ['avatar0']

    def generate(self, avatars, text, usernames, kwargs):
        avatar = http.get_image(avatars[0]).convert('RGBA').resize((256, 256))

        salt = (
            Image.open(self.assets.get('assets/salty/salt.bmp'))
            .convert('RGBA')
            .resize((256, 256))
            .rotate(-130, resample=Image.BICUBIC)
        )

        blank = Image.new('RGBA', (256, 256))
        blank.paste(avatar, (0, 0), avatar)
        frames = []

        for i in range(8):
            base = blank.copy()
            if i == 0:
                base.paste(salt, (-125, -125), salt)
            else:
                base.paste(salt, (-135 + randint(-5, 5), -135 + randint(-5, 5)), salt)

            frames.append(base)

        b = BytesIO()
        frames[0].save(b, save_all=True, append_images=frames[1:], format='gif', loop=0, duration=20,
                       optimize=True)
        b.seek(0)
        return send_file(b, mimetype='image/gif')
