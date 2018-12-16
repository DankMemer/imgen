from io import BytesIO

from PIL import Image, ImageDraw
from flask import send_file

from utils.endpoint import Endpoint, setup
from utils.textutils import auto_text_size


@setup
class Boo(Endpoint):
    params = ['text']

    def generate(self, avatars, text, usernames, kwargs):
        base = Image.open(self.assets.get('assets/boo/boo.bmp')).convert('RGBA')
        # We need a text layer here for the rotation
        canv = ImageDraw.Draw(base)

        text = text.split(', ')

        if len(text) != 2:
            text = ["Separate the items with a", "comma followed by a space"]

        first, second = text

        first_font, first_text = auto_text_size(first,
                                                self.assets.get_font('assets/fonts/sans.ttf'), 144,
                                                font_scalar=0.7)
        second_font, second_text = auto_text_size(second,
                                                  self.assets.get_font('assets/fonts/sans.ttf'),
                                                  144,
                                                  font_scalar=0.7)

        canv.text((35, 54), first_text, font=first_font, fill='Black')
        canv.text((267, 57), second_text, font=second_font, fill='Black')
        base = base.convert('RGB')

        b = BytesIO()
        base.save(b, format='jpeg')
        b.seek(0)
        return send_file(b, mimetype='image/jpeg')
