from io import BytesIO

from flask import send_file
from PIL import Image

from utils import http
from utils.endpoint import Endpoint


class Spank(Endpoint):
    def generate(self, avatars, text, usernames):
        base = Image.open('assets/spank/spank.jpg').resize((500, 500))
        img1 = http.get_image(avatars[0]).resize((140, 140)).convert('RGBA')
        img2 = http.get_image(avatars[1]).resize((120, 120)).convert('RGBA')
        base.paste(img1, (225, 5), img1)
        base.paste(img2, (350, 220), img2)

        b = BytesIO()
        base.save(b, format='png')
        b.seek(0)
        return send_file(b, mimetype='image/png')


def setup():
    return Spank()
