from io import BytesIO

from PIL import Image
from flask import send_file

from utils import http
from utils.endpoint import Endpoint, setup


@setup
class Hitler(Endpoint):
    params = ['avatar0']

    def generate(self, avatars, text, usernames, kwargs):
        base = Image.open(self.assets.get('assets/hitler/hitler.bmp'))
        img1 = http.get_image(avatars[0]).convert('RGBA').resize((140, 140))
        base.paste(img1, (46, 43), img1)
        base = base.convert('RGB')

        b = BytesIO()
        base.save(b, format='png')
        b.seek(0)
        return send_file(b, mimetype='image/png')
