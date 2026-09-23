import uuid
import os
from flask import send_file, after_this_request
from numpy import array

from utils.endpoint import Endpoint, setup
from utils.video_text import render_video_text

from moviepy.editor import VideoFileClip, ImageClip, CompositeVideoClip


@setup(rate=1, per=30)
class Crab(Endpoint):
    """
    This endpoint returns an MP4 file. Make sure your application knows how to handle this format.
    Malformed requests count against your ratelimit for this endpoint.
    """
    params = ['text1', 'text2']

    def generate(self, avatars, text, usernames, kwargs):
        name = uuid.uuid4().hex + '.mp4'

        @after_this_request
        def remove(response):  # pylint: disable=W0612
            try:
                os.remove(name)
            except (FileNotFoundError, OSError, PermissionError):
                pass

            return response

        t = [value.upper() for value in self.text_fields(kwargs, 2)]
        clip = VideoFileClip("assets/crab/template.mp4")
        text = ImageClip(array(render_video_text(t[0], 'Symbola', 48, 'white')))
        text2 = ImageClip(array(render_video_text("____________________", 'Verdana', 48, 'white')))\
            .set_position(("center", 210)).set_duration(15.4)
        text = text.set_position(("center", 200)).set_duration(15.4)
        text3 = ImageClip(array(render_video_text(t[1], 'Verdana', 48, 'white')))\
            .set_position(("center", 270)).set_duration(15.4)

        video = CompositeVideoClip([clip, text.crossfadein(1), text2.crossfadein(1), text3.crossfadein(1)]).set_duration(15.4)

        video.write_videofile(name, threads=4, preset='superfast', verbose=False)
        clip.close()
        video.close()
        return send_file(name, mimetype='video/mp4')
