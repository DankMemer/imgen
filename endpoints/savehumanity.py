from io import BytesIO

from PIL import Image, ImageDraw
from flask import send_file

from utils.endpoint import Endpoint, setup
from utils.textutils import wrap, render_text_with_emoji


@setup
class SaveHumanity(Endpoint):
    params = ['text']

    def generate(self, avatars, text, usernames, kwargs):
        base = Image.open(self.assets.get('assets/humanity/humanity.bmp')).convert('RGBA')
        # We need a text layer here for the rotation
        text_layer = Image.new('RGBA', base.size)
        font = self.assets.get_font('assets/fonts/sans.ttf', size=16)
        canv = ImageDraw.Draw(text_layer)

        text = wrap(font, text, 180)
        render_text_with_emoji(text_layer, canv, (490, 410), text, font=font, fill='Black')

        text_layer = text_layer.rotate(-7, resample=Image.BICUBIC)

        base.paste(text_layer, (0, 0), text_layer)
        base = base.convert('RGB')

        b = BytesIO()
        base.save(b, format='jpeg')
        b.seek(0)
        return send_file(b, mimetype='image/jpeg')
