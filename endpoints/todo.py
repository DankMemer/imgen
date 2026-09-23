from io import BytesIO

from flask import send_file
from PIL import Image

from utils.endpoint import Endpoint, setup
from utils.template_text import draw_fitted_text


@setup
class Todo(Endpoint):
    params = ['text']

    def generate(self, avatars, text, usernames, kwargs):
        image = Image.open(self.assets.get('assets/todo/todo.jpg')).convert('RGB')
        layer = Image.new('RGBA', (360, 220))
        font = lambda size: self.assets.get_font('assets/fonts/arimobold.ttf', size=size)
        draw_fitted_text(layer, text, (8, 4, 352, 215), font, 34, max_lines=8)
        layer = layer.rotate(15, resample=Image.BICUBIC, expand=True)
        image.paste(layer, (345, 215), layer)

        output = BytesIO()
        image.save(output, format='JPEG', quality=92)
        output.seek(0)
        return send_file(output, mimetype='image/jpeg')
