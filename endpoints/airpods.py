from io import BytesIO

from flask import send_file
from PIL import Image

from utils import http
from utils.endpoint import Endpoint, setup


@setup
class Airpods(Endpoint):
    params = ['avatar0']

    def generate(self, avatars, text, usernames, kwargs):
        blank = Image.new('RGBA', (400, 128), (255, 255, 255, 0))
        avatar = http.get_image(avatars[0]).convert('RGBA').resize((128, 128))
        left = Image.open('assets/airpods/left.gif')
        right = Image.open('assets/airpods/right.gif')
        out = []
        for i in range(0, left.n_frames):
            left.seek(i)
            right.seek(i)
            f = blank.copy().convert('RGBA')
            l = left.copy().convert('RGBA')
            r = right.copy().convert('RGBA')
            f.paste(l, (0, 0), l)
            f.paste(avatar, (136, 0), avatar)
            f.paste(r, (272, 0), r)
            out.append(f.resize((400, 128), Image.LANCZOS).convert('RGBA'))

        b = BytesIO()
        out[0].save(b, format='gif', save_all=True, append_images=out[1:], loop=0, disposal=2, optimize=True,
                    duration=30, transparency=0)
        b.seek(0)
        return send_file(b, mimetype='image/gif')
