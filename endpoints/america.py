from io import BytesIO

from flask import send_file
from PIL import Image

from utils import http
from utils.endpoint import Endpoint, setup


@setup
class America(Endpoint):
    params = ['avatar0']

    def generate(self, avatars, text, usernames, kwargs):
        img1 = http.get_image(avatars[0]).convert('RGBA').resize((480, 480))
        img2 = Image.open('assets/america/america.gif')
        img1.putalpha(128)

        out = []
        for i in range(0, img2.n_frames):
            img2.seek(i)
            f = img2.copy().convert('RGBA').resize((480, 480))
            f.paste(img1, (0, 0), img1)
            out.append(f.resize((256, 256)))

        b = BytesIO()
        out[0].save(b, format='gif', save_all=True, append_images=out[1:], loop=0, disposal=2, optimize=True, duration=30)
        b.seek(0)
        return send_file(b, mimetype='image/gif')
