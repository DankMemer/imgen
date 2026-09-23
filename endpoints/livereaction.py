from io import BytesIO

from flask import send_file
from PIL import Image, ImageOps

from utils import http
from utils.endpoint import Endpoint, setup
from utils.exceptions import BadRequest
from utils.template_text import draw_fitted_text


@setup
class LiveReaction(Endpoint):
    params = ['avatar0', 'text']

    def generate(self, avatars, text, usernames, kwargs):
        if not avatars:
            raise BadRequest('Provide avatar1.')
        image = Image.open(self.assets.get('assets/livereaction/livereaction.png')).convert('RGB')
        inset = ImageOps.fit(http.get_image(avatars[0]).convert('RGB'), (929, 526), method=Image.LANCZOS)
        image.paste(inset, (15, 164))
        font = lambda size: self.assets.get_font('assets/fonts/arimobold.ttf', size=size)
        draw_fitted_text(image, text.upper(), (207, 16, 524, 146), font, 120, minimum=7, max_lines=1, fill='white')

        output = BytesIO()
        image.save(output, format='PNG')
        output.seek(0)
        return send_file(output, mimetype='image/png')
