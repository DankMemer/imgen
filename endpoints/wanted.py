from io import BytesIO

from flask import send_file
from PIL import Image

from utils import http
from utils.endpoint import Endpoint


class Wanted(Endpoint):
    def generate(self, avatars, text, usernames):
        base = Image.open('assets/Wanted/wanted.png').convert('RGBA')
        avatar = Image.open(http.get_image(avatars[0])).resize((447, 447)).convert('RGBA')
        base.paste(avatar, (145, 282), avatar)

        b = BytesIO()
        base.save(b, format='png')
        b.seek(0)
        return send_file(b, mimetype='image/png')


def setup():
    return Wanted()
