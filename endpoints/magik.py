from io import BytesIO

from flask import send_file
from wand import image

from utils import http
from utils.endpoint import Endpoint, setup


@setup
class Magik(Endpoint):
    params = ['avatar0']

    def generate(self, avatars, text, usernames, kwargs):
        avatar = BytesIO(http.get_content_raw(avatars[0]))
        with image.Image(file=avatar) as img:
            if img.animation:
                img = img.convert('png')
            img.transform(resize='400x400')
            try:
                multiplier = int(text)
            except ValueError:
                multiplier = 1
            else:
                multiplier = max(min(multiplier, 10), 1)
            img.liquid_rescale(width=int(img.width * 0.5),
                               height=int(img.height * 0.5),
                               delta_x=0.5 * multiplier,
                               rigidity=0)
            img.liquid_rescale(width=int(img.width * 1.5),
                               height=int(img.height * 1.5),
                               delta_x=2 * multiplier,
                               rigidity=0)

            b = BytesIO()
            img.save(file=b)
            b.seek(0)
            return send_file(b, mimetype='image/png')
