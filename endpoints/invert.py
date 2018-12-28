from io import BytesIO

from PIL import Image, ImageOps
from flask import send_file

from utils import http
from utils.endpoint import Endpoint, setup


@setup
class Invert(Endpoint):
    params = ['avatar0']

    def generate(self, avatars, text, usernames, kwargs):
        img = http.get_image(avatars[0])
        if img.mode == 'RGBA':
            r, g, b, a = img.split()
            rgb_image = Image.merge('RGB', (r, g, b))
            inverted = ImageOps.invert(rgb_image)
            r, g, b = inverted.split()
            img = Image.merge('RGBA', (r, g, b, a))
        else:
            img = img.convert('RGB')
            img = ImageOps.invert(img)

        img = img.convert('RGBA')
        b = BytesIO()
        img.save(b, format='png')
        b.seek(0)
        return send_file(b, mimetype='image/png')
