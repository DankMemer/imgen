from io import BytesIO
from random import randint

from PIL import Image
from PIL import ImageOps
from flask import send_file

from utils import http
from utils.endpoint import Endpoint


class Dank(Endpoint):
    def generate(self, avatars, text, usernames):
        avatar = http.get_image(avatars[0]).resize((320, 320)).convert('RGBA')

        horn = Image.open('assets/dank/horn.png').convert('RGBA').resize((100, 100)).rotate(315, resample=Image.BICUBIC)
        horn2 = ImageOps.mirror(horn.copy().resize((130, 130)).rotate(350, resample=Image.BICUBIC))
        hit = Image.open('assets/dank/hit.png').convert('RGBA').resize((40, 40))
        gun = Image.open('assets/dank/gun.png').convert('RGBA').resize((250, 205))
        faze = Image.open('assets/dank/faze.png').convert('RGBA').resize((60, 40))

        blank = Image.new('RGBA', (256, 256), color=(254, 0, 0))
        blank.paste(avatar, (-20, -20), avatar)
        # blank.paste(overlay, None, overlay)
        frames = []

        for i in range(8):
            base = blank.copy()
            if i == 0:
                base.paste(horn, (175, 0), horn)
                base.paste(horn2, (-60, 0), horn2)
                base.paste(hit, (90, 65), hit)
                base.paste(gun, (120, 130), gun)
                base.paste(faze, (5, 212), faze)
            else:
                base.paste(horn, (165 + randint(-8, 8), randint(0, 12)), horn)
                base.paste(horn2, (-50 + randint(-6, 6), randint(-2, 10)), horn2)
                base.paste(hit, (110 + randint(-30, 30), 55 + randint(-30, 30)), hit)
                base.paste(gun, (120, 130), gun)
                base.paste(faze, (12 + randint(-6, 6), 210 + randint(-2, 10)), faze)

            frames.append(base)

        b = BytesIO()
        frames[0].save(b, save_all=True, append_images=frames[1:], format='gif', loop=0, duration=20,
                       optimize=True)
        b.seek(0)
        return send_file(b, mimetype='image/gif')


def setup():
    return Dank()
