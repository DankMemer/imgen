from io import BytesIO

from flask import send_file
from PIL import Image, ImageDraw, ImageOps

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
        inset = ImageOps.fit(http.get_image(avatars[0]).convert('RGB'), (832, 454), method=Image.LANCZOS)
        mask = Image.new('L', inset.size)
        ImageDraw.Draw(mask).rounded_rectangle((0, 0, 831, 453), radius=25, fill=255)
        image.paste(inset, (64, 202), mask)
        draw = ImageDraw.Draw(image)
        draw.rounded_rectangle((63, 201, 896, 656), radius=26, outline='white', width=3)
        font = lambda size: self.assets.get_font('assets/fonts/arimobold.ttf', size=size)
        draw_fitted_text(image, text.upper(), (207, 16, 524, 146), font, 120, minimum=7, max_lines=1, fill='white')

        output = BytesIO()
        image.save(output, format='PNG')
        output.seek(0)
        return send_file(output, mimetype='image/png')
