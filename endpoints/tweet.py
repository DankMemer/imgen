from io import BytesIO

from PIL import Image, ImageDraw
from flask import send_file

from utils.endpoint import Endpoint
from utils.textutils import wrap


class Tweet(Endpoint):
    def generate(self, avatars, text, usernames):
        base = Image.open(self.assets.get('assets/tweet/trump.bmp'))
        font = self.assets.get_font('assets/fonts/segoeuireg.ttf', size=50)
        canv = ImageDraw.Draw(base)
        text = wrap(font, text, 1150)
        canv.text((45, 160), text, font=font, fill='Black')
        base = base.convert('RGB')

        b = BytesIO()
        base.save(b, format='jpeg')
        b.seek(0)
        return send_file(b, mimetype='image/jpeg')


def setup(cache):
    return Tweet(cache)
