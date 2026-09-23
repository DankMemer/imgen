from io import BytesIO

from flask import send_file
from PIL import Image

from utils.endpoint import Endpoint, setup
from utils.template_text import draw_fitted_text


@setup
class Machine(Endpoint):
    params = ['text1', 'text2']

    def generate(self, avatars, text, usernames, kwargs):
        first, second = self.text_fields(kwargs, 2)
        image = Image.open(self.assets.get('assets/machine/machine.png')).convert('RGB')
        font = lambda size: self.assets.get_font('assets/fonts/arimobold.ttf', size=size)
        draw_fitted_text(image, first, (299, 468, 820, 585), font, 39, max_lines=2, fill='white')
        draw_fitted_text(image, second, (175, 792, 820, 888), font, 42, max_lines=3, fill='white')

        output = BytesIO()
        image.save(output, format='PNG')
        output.seek(0)
        return send_file(output, mimetype='image/png')
