from io import BytesIO

from PIL import Image, ImageDraw
from flask import send_file

from utils import http
from utils.endpoint import Endpoint, setup
from utils.textutils import wrap, render_text_with_emoji


@setup
class Byemom(Endpoint):
    params = ['avatar0', 'username0', 'text']

    def generate(self, avatars, text, usernames, kwargs):
        base = Image.open(self.assets.get('assets/byemom/mom.bmp'))
        avatar = http.get_image(avatars[0]).convert('RGBA').resize((70, 70), resample=Image.BICUBIC)
        avatar2 = avatar.copy().resize((125, 125), resample=Image.BICUBIC)
        text_layer = Image.new('RGBA', (350, 25))
        bye_layer = Image.new('RGBA', (180, 51), (255, 255, 255))
        font = self.assets.get_font('assets/fonts/arial.ttf', size=20)
        bye_font = self.assets.get_font('assets/fonts/arimobold.ttf', size=14)
        canv = ImageDraw.Draw(text_layer)
        bye = ImageDraw.Draw(bye_layer)
        username = usernames[0] or 'Tommy'
        msg = 'Alright {} im leaving the house to run some errands'.format(username)

        text = wrap(font, text, 500)
        msg = wrap(font, msg, 200)

        render_text_with_emoji(text_layer, canv, (0, 0), text, font=font, fill='Black')
        render_text_with_emoji(bye_layer, bye, (0, 0), msg, font=bye_font, fill=(42, 40, 165))
        text_layer = text_layer.rotate(24.75, resample=Image.BICUBIC, expand=True)

        base.paste(text_layer, (350, 443), text_layer)
        base.paste(bye_layer, (150, 7))
        base.paste(avatar, (530, 15), avatar)
        base.paste(avatar2, (70, 340), avatar2)
        base = base.convert('RGBA')

        b = BytesIO()
        base.save(b, format='png')
        b.seek(0)
        return send_file(b, mimetype='image/png')
