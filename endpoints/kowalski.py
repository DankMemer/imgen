import uuid
import os
from flask import send_file, after_this_request
from numpy import array

from utils.endpoint import Endpoint, setup
from utils.video_text import render_video_text

from moviepy.editor import VideoFileClip, ImageClip, CompositeVideoClip
from moviepy.video.fx.rotate import rotate


@setup(rate=1, per=30)
class Kowalski(Endpoint):
    """
    This endpoint returns a GIF file.
    Malformed requests count against your ratelimit for this endpoint.
    """
    params = ['text']

    def generate(self, avatars, text, usernames, kwargs):
        name = uuid.uuid4().hex + '.gif'

        @after_this_request
        def remove(response):  # pylint: disable=W0612
            try:
                os.remove(name)
            except (FileNotFoundError, OSError, PermissionError):
                pass

            return response
        clip = VideoFileClip("assets/kowalski/kowalski.gif")
        text = ImageClip(array(render_video_text(text, 'Verdana', 36, 'black', width=245, stroke_width=1)))\
            .set_duration(clip.duration)
        text = text.set_position((340, 65)).set_duration(clip.duration)
        text = rotate(text, angle=10, resample='bilinear')

        video = CompositeVideoClip([clip, text]).set_duration(clip.duration)

        video.write_gif(name)
        clip.close()
        video.close()
        return send_file(name, mimetype='image/gif')
