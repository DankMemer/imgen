from io import BytesIO

from PIL import Image, ImageDraw
from flask import send_file

from utils.endpoint import Endpoint, setup
from utils.textutils import auto_text_size, render_text_with_emoji


@setup
class Balloon(Endpoint):
    params = ['text']

    def generate(self, avatars, text, usernames, kwargs):
        base = Image.open(self.assets.get('assets/balloon/balloon.bmp')).convert('RGBA')
        font = self.assets.get_font('assets/fonts/sans.ttf')
        canv = ImageDraw.Draw(base)

        text = text.split(', ')

        if len(text) != 2:
            text = ["Separate the items with a", "comma followed by a space"]

        balloon, label = text

        balloon_text_1_font, balloon_text_1 = auto_text_size(balloon, font, 162)
        balloon_text_2_font, balloon_text_2 = auto_text_size(balloon, font, 170, font_scalar=0.95)
        balloon_text_3_font, balloon_text_3 = auto_text_size(balloon, font, 110, font_scalar=0.8)
        label_font, label_text = auto_text_size(label, font, 125)

        render_text_with_emoji(base, canv, (80, 180), balloon_text_1, font=balloon_text_1_font, fill='Black')
        render_text_with_emoji(base, canv, (50, 530), balloon_text_2, font=balloon_text_2_font, fill='Black')
        render_text_with_emoji(base, canv, (500, 520), balloon_text_3, font=balloon_text_3_font, fill='Black')
        render_text_with_emoji(base, canv, (620, 155), label_text, font=label_font, fill='Black')
        base = base.convert('RGB')

        b = BytesIO()
        base.save(b, format='jpeg')
        b.seek(0)
        return send_file(b, mimetype='image/jpeg')
