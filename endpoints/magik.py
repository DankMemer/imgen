from io import BytesIO

from flask import send_file
from wand import image

from utils import http
from utils.endpoint import Endpoint


class Magik(Endpoint):
    def generate(self, avatars, text, usernames):
        avatar = BytesIO(http.get_image_raw(avatars[0]))
        with image.Image(file=avatar) as img:
            img.transform(resize='400x400')
            img.liquid_rescale(width=int(img.width * 0.5),
                               height=int(img.height * 0.5),
                               delta_x=0.5,
                               rigidity=0)
            img.liquid_rescale(width=int(img.width * 1.5),
                               height=int(img.height * 1.5),
                               delta_x=2,
                               rigidity=0)

            b = BytesIO()
            img.save(file=b)
            b.seek(0)
            return send_file(b, mimetype='image/png')


def setup():
    return Magik()
