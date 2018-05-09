from io import BytesIO

from flask import send_file
from PIL import Image

from utils import http
from utils.endpoint import Endpoint


class Gay(Endpoint):
    def generate(self, *args):
        img1 = Image.open(http.get_image(args[0]))
        img2 = Image.open('assets/gay/gay.png').convert('RGBA').resize(img1.size)
        img2.putalpha(128)
        img1.paste(img2, (0, 0), img2)

        b = BytesIO()
        img1.save(b, format='png')
        b.seek(0)
        return send_file(b, mimetype='image/png', attachment_filename=f'{self.name}.png')


def setup():
    return Gay()
