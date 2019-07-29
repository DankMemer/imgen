from io import BytesIO

from PIL import Image, ImageDraw
from flask import send_file

from utils.endpoint import Endpoint, setup
from utils.textutils import render_text_with_emoji, wrap


@setup
class JustPretending(Endpoint):
    params = ['text']

    def generate(self, avatars, text, usernames, kwargs):
        text = text.replace(', ', ',').split(',')
        if len(text) != 2:
            text = ['you should add two things split by commas', 'idiot']
        base = Image.open(self.assets.get('assets/justpretending/justpretending.jpg'))
        font = self.assets.get_font('assets/fonts/verdana.ttf', size=24)
        canv = ImageDraw.Draw(base)
        render_text_with_emoji(base, canv, (678, 12), wrap(font, text[0], 320), font, 'black')
        render_text_with_emoji(base, canv, (9, 800), wrap(font, text[1], 100), font, 'black')
        render_text_with_emoji(base, canv, (399, 808), wrap(font, text[1], 100), font, 'black')
        render_text_with_emoji(base, canv, (59, 917), wrap(font, text[1], 100), font, 'black')
        render_text_with_emoji(base, canv, (425, 910), wrap(font, text[1], 100), font, 'black')

        base = base.convert('RGB')
        b = BytesIO()
        base.save(b, format='jpeg')
        b.seek(0)
        return send_file(b, mimetype='image/jpeg')
