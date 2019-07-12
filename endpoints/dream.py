from io import BytesIO

from PIL import Image
from flask import send_file

from utils.endpoint import Endpoint, setup
from utils.deep_dream import render_dream
from utils import http


# @setup(rate=1, per=20)
class Dream(Endpoint):
    """This endpoint deep dreams your input image. This endpoint has a seperate ratelimit of 1 request per 20 seconds
    due to CPU and high generation time. Generating a deep dream can take anywhere between 10 and 20 seconds"""
    params = ['avatar0']

    def generate(self, avatars, text, usernames, kwargs):
        avatar = http.get_image(avatars[0]).convert('RGB')
        if avatar.height <= 300:  # do not use rofl
            avatar = avatar.resize((avatar.width * 2, avatar.height * 2), Image.LANCZOS)
        elif avatar.height <= 600:
            avatar = avatar.resize((avatar.width, avatar.height), Image.LANCZOS)
        elif avatar.height > 1200:
            avatar = avatar.resize((int(avatar.width / 2), int(avatar.height / 2)), Image.LANCZOS)
        f = render_dream(avatar)
        base = Image.fromarray(f)
        b = BytesIO()
        base.save(b, format='jpeg')
        b.seek(0)
        return send_file(b, mimetype='image/jpeg')
