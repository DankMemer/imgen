from io import BytesIO

from PIL import Image, ImageDraw
from flask import send_file

from utils.endpoint import Endpoint, setup
from utils.textutils import render_text_with_emoji, wrap


@setup
class Farmer(Endpoint):
    params = ['text']

    def generate(self, avatars, text, usernames, kwargs):
        base = Image.open(self.assets.get('assets/farmer/farmer.jpg'))
        font = self.assets.get_font('assets/fonts/verdana.ttf', size=24)
        canv = ImageDraw.Draw(base)

        clouds, farmer = text.replace(', ', ',').split(',', 1)

        if len(clouds) >= 150:
            clouds = clouds[:147] + '...'

        if len(farmer) >= 100:
            farmer = farmer[:97] + '...'
        render_text_with_emoji(base, canv, (50, 300), wrap(font, clouds, 580), font, 'white')
        render_text_with_emoji(base, canv, (50, 825), wrap(font, farmer, 580), font, 'white')

        base = base.convert('RGB')
        b = BytesIO()
        base.save(b, format='jpeg')
        b.seek(0)
        return send_file(b, mimetype='image/jpeg')
