from io import BytesIO

from PIL import Image, ImageDraw
from flask import send_file

from utils.endpoint import Endpoint, setup
from utils.textutils import auto_text_size


@setup
class Vr(Endpoint):
    params = ['text']

    def generate(self, avatars, text, usernames, kwargs):
        base = Image.open(self.assets.get('assets/vr/vr.bmp')).convert('RGBA')
        # We need a text layer here for the rotation
        font, text = auto_text_size(text, self.assets.get_font('assets/fonts/sans.ttf'), 207, font_scalar=0.8)
        canv = ImageDraw.Draw(base)
        w, _ = canv.textsize(text, font)
        canv.multiline_text(((170 - (w/2)), 485), text, font=font, fill='Black', anchor='center', align='center')
        base = base.convert('RGB')

        b = BytesIO()
        base.save(b, format='jpeg')
        b.seek(0)
        return send_file(b, mimetype='image/jpeg')
