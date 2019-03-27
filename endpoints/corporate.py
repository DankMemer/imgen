from io import BytesIO

from PIL import Image
from flask import send_file

from utils import http
from utils.endpoint import Endpoint, setup
from utils.skew import skew


@setup
class Corporate(Endpoint):
    params = ['avatar0']

    def generate(self, avatars, text, usernames, kwargs):
        base = Image.open(self.assets.get('assets/corporate/corporate.jpg'))
        img1 = http.get_image(avatars[0]).convert('RGBA').resize((512, 512), Image.LANCZOS)
        try:
            img2 = http.get_image(avatars[1]).convert('RGBA').resize((512, 512), Image.LANCZOS)
        except IndexError:
            img2 = img1

        img1 = skew(img1, [(208, 44), (718, 84), (548, 538), (20, 446)])

        img2 = skew(img2, [(858, 112), (1600, 206), (1312, 666), (634, 546)], resolution=1400)

        base.paste(img1, (0, 0), img1)
        base.paste(img2, (0, 0), img2)

        base = base.resize((base.width // 2, base.height // 2))

        b = BytesIO()
        base.save(b, format='png')
        b.seek(0)
        return send_file(b, mimetype='image/png')
