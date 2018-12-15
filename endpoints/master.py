from io import BytesIO

from PIL import Image, ImageDraw
from flask import send_file

from utils.endpoint import Endpoint, setup
from utils.textutils import auto_text_size


@setup
class Master(Endpoint):
    params = ['text']

    def generate(self, avatars, text, usernames, kwargs):
        base = Image.open(self.assets.get('assets/master/master.bmp')).convert('RGBA')
        text = text.split(',')
        if len(text) == 3:
            a, b, c = text
        else:
            a, b, c = ('you need 3 items', 'for this command', 'split by commas')
        font, text1 = auto_text_size(a, self.assets.get_font('assets/fonts/sans.ttf'), 250, font_scalar=0.2)
        font, text2 = auto_text_size(b, font, 250, font_scalar=0.3)
        font, text3 = auto_text_size(c, font, 300, font_scalar=0.2)
        canv = ImageDraw.Draw(base)
        text_layer = Image.new('RGBA', base.size)
        tilted_text = ImageDraw.Draw(text_layer)

        canv.text((457, 513), text1, font=font, fill='White')
        tilted_text.text((350, 330), text2, font=font, fill='White')
        canv.text((148, 151), text3, font=font, fill='White')

        text_layer = text_layer.rotate(8, resample=Image.BICUBIC)

        base.paste(text_layer, (0, 0), text_layer)
        base = base.convert('RGB')

        b = BytesIO()
        base.save(b, format='jpeg')
        b.seek(0)
        return send_file(b, mimetype='image/jpeg')
