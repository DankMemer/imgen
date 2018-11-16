from io import BytesIO

from flask import send_file
from PIL import Image

from utils import http
from utils.endpoint import Endpoint


class Jail(Endpoint):
    def generate(self, avatars, text, usernames):
        overlay = Image.open(self.assets.get('assets/jail/jail.bmp')).resize((350, 350))
        base = http.get_image(avatars[0]).convert('LA').resize((350, 350))
        base.paste(overlay, (0, 0), overlay)

        base = base.convert('RGB')
        b = BytesIO()
        base.save(b, format='jpeg')
        b.seek(0)
        return send_file(b, mimetype='image/jpeg')


def setup(cache):
    return Jail(cache)
