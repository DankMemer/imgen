import os
import uuid

from flask import after_this_request, send_file
from moviepy.editor import CompositeVideoClip, ImageClip, VideoFileClip
from numpy import array
from PIL import Image

from utils.endpoint import Endpoint, setup
from utils.template_text import draw_fitted_text


@setup(rate=1, per=30)
class ScaryAbove(Endpoint):
    params = ['text']

    def generate(self, avatars, text, usernames, kwargs):
        caption = Image.new('RGBA', (498, 99))
        font = lambda size: self.assets.get_font('assets/fonts/arimobold.ttf', size=size)
        draw_fitted_text(caption, text, (10, 2, 488, 97), font, 32, max_lines=3)
        name = uuid.uuid4().hex + '.mp4'

        @after_this_request
        def remove(response):
            try:
                os.remove(name)
            except (FileNotFoundError, OSError, PermissionError):
                pass
            return response

        source = VideoFileClip('assets/scaryabove/scaryabove.mp4')
        overlay = ImageClip(array(caption)).set_duration(source.duration)
        video = CompositeVideoClip([source, overlay])
        try:
            video.write_videofile(name, threads=2, preset='superfast', verbose=False, logger=None)
        finally:
            video.close()
            source.close()
        return send_file(name, mimetype='video/mp4')
