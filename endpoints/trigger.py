from io import BytesIO
from random import randint

from flask import send_file
from PIL import Image

from utils import http
from utils.endpoint import Endpoint


class Trigger(Endpoint):
    def generate(self, avatars, text, usernames):
        avatar = http.get_image(avatars[0]).resize((320, 320)).convert('RGBA')
        triggered = Image.open('assets/triggered/triggered.jpg')
        tint = Image.open('assets/triggered/red.png').convert('RGBA')
        blank = Image.new('RGBA', (256, 256), color=(231, 19, 29))
        frames = []

        for i in range(8):
            base = blank.copy()

            if i == 0:
                base.paste(avatar, (-16, -16), avatar)
            else:
                base.paste(avatar, (-32 + randint(-16, 16), -32 + randint(-16, 16)), avatar)

            base.paste(tint, (0, 0), tint)

            if i == 0:
                base.paste(triggered, (-10, 200))
            else:
                base.paste(triggered, (-12 + randint(-8, 8), 200 + randint(0, 12)))

            frames.append(base)

        b = BytesIO()
        frames[0].save(b, save_all=True, append_images=frames[1:], format='gif', loop=0, duration=20, disposal=2, optimize=True)
        b.seek(0)
        return send_file(b, mimetype='image/gif')


def setup():
    return Trigger()
