from io import BytesIO

from flask import send_file
from PIL import Image

from utils.endpoint import Endpoint, setup
from utils.template_text import draw_fitted_text


@setup
class Jarvis(Endpoint):
    params = ['text']

    def generate(self, avatars, text, usernames, kwargs):
        image = Image.open(self.assets.get('assets/jarvis/jarvis.jpg')).convert('RGB')
        font = lambda size: self.assets.get_font('assets/fonts/arimobold.ttf', size=size)
        draw_fitted_text(image, text, (20, 14, 620, 194), font, 46, max_lines=4)

        output = BytesIO()
        image.save(output, format='JPEG', quality=92)
        output.seek(0)
        return send_file(output, mimetype='image/jpeg')
