from io import BytesIO

from flask import send_file
from PIL import Image

from utils import http
from utils.endpoint import Endpoint


class Jail(Endpoint):
    def generate(self, avatars, text, usernames):
        overlay = Image.open('assets/jail/jail.png').resize((350, 350))
        base = http.get_image(avatars[0]).convert('LA').resize((350, 350))
        base.paste(overlay, (0, 0), overlay)

        b = BytesIO()
        base.save(b, format='png')
        b.seek(0)
        return send_file(b, mimetype='image/png')


def setup():
    return Jail()
