from io import BytesIO

from flask import send_file
from PIL import Image

from utils import http
from utils.endpoint import Endpoint


class Hitler(Endpoint):
    def generate(self, avatars, text, usernames):
        base = Image.open('assets/hitler/hitler.jpeg')
        img1 = http.get_image(avatars[0]).convert('RGBA').resize((140, 140))
        base.paste(img1, (46, 43), img1)

        b = BytesIO()
        base.save(b, format='png')
        b.seek(0)
        return send_file(b, mimetype='image/png')


def setup():
    return Hitler()
