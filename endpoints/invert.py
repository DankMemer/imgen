from io import BytesIO

from flask import send_file
from PIL import Image, ImageOps

from utils import http
from utils.endpoint import Endpoint


class Invert(Endpoint):
    def generate(self, avatars, text, usernames):
        img = http.get_image(avatars[0])
        if img.mode == 'RGBA':
            r, g, b, a = img.split()
            rgb_image = Image.merge('RGB', (r, g, b))
            inverted = ImageOps.invert(rgb_image)
            r, g, b = inverted.split()
            img = Image.merge('RGBA', (r, g, b, a))
        else:
            img = ImageOps.invert(img)

        b = BytesIO()
        img.save(b, format='png')
        b.seek(0)
        return send_file(b, mimetype='image/png')


def setup():
    return Invert()
