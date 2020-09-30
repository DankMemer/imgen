import uuid
import os
from flask import send_file, after_this_request

from utils.endpoint import Endpoint, setup
from utils.exceptions import BadRequest
from utils import http
from utils.textutils import wrap

from moviepy.editor import VideoFileClip, ImageClip, CompositeVideoClip, TextClip, ColorClip


@setup(rate=1, per=30)
class LetMeIn(Endpoint):
    """
    This endpoint returns an MP4 file. Make sure your application knows how to handle this format.
    Malformed requests count against your ratelimit for this endpoint.
    """
    params = ['text']

    def generate(self, avatars, text, usernames, kwargs):
        name = uuid.uuid4().hex + '.mp4'
        if len(text) >= 400:
            text = text[:400] + '...'

        @after_this_request
        def remove(response):  # pylint: disable=W0612
            try:
                os.remove(name)
            except (FileNotFoundError, OSError, PermissionError):
                pass

            return response

        clip = VideoFileClip("assets/letmein/letmein.mp4")



        textclip = TextClip(txt=text, bg_color='White', fontsize=32, font='Verdana', method='caption', align='west', size=(clip.size[0], None)).set_duration(clip.duration)

        color = ColorClip((clip.size[0], textclip.size[1]), color=(255, 255, 255), ismask=False).set_duration(clip.duration)

        video = CompositeVideoClip([clip.set_position(("center", textclip.size[1])), color, textclip],
                                   size=(clip.size[0], textclip.size[1] + clip.size[1]))

        video.write_videofile(name, threads=4, preset='superfast', verbose=False)
        clip.close()
        video.close()
        return send_file(name, mimetype='video/mp4')
