from io import BytesIO

from PIL import Image, ImageDraw
from flask import send_file

from utils.endpoint import Endpoint, setup
from utils.textutils import auto_text_size, render_text_with_emoji


@setup
class KnowYourLocation(Endpoint):
    params = ['text1', 'text2']

    def generate(self, avatars, text, usernames, kwargs):
        base = Image.open(self.assets.get('assets/knowyourlocation/knowyourlocation.bmp')).convert('RGBA')
        # We need a text layer here for the rotation
        canv = ImageDraw.Draw(base)

        top, bottom = self.text_fields(kwargs, 2)

        top_font, top_text = auto_text_size(top, self.assets.get_font('assets/fonts/sans.ttf'), 630)
        bottom_font, bottom_text = auto_text_size(bottom,
                                                  self.assets.get_font('assets/fonts/sans.ttf'),
                                                  539)
        render_text_with_emoji(base, canv, (64, 131), top_text, top_font, 'black')
        render_text_with_emoji(base, canv, (120, 450), bottom_text, bottom_font, 'black')
        base = base.convert('RGB')

        b = BytesIO()
        base.save(b, format='jpeg')
        b.seek(0)
        return send_file(b, mimetype='image/jpeg')
