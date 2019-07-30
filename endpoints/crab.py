import uuid
import os
from flask import send_file, after_this_request

from utils.endpoint import Endpoint, setup
from utils.exceptions import BadRequest

from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip


@setup(rate=1, per=30)
class Crab(Endpoint):
    """
    This endpoint returns an MP4 file. Make sure your application knows how to handle this format.
    Malformed requests count against your ratelimit for this endpoint.
    Separate text with a comma.
    """
    params = ['text']

    def generate(self, avatars, text, usernames, kwargs):
        name = uuid.uuid4().hex + '.mp4'

        @after_this_request
        def remove(response):  # pylint: disable=W0612
            try:
                os.remove(name)
            except (FileNotFoundError, OSError, PermissionError):
                pass

            return response

        t = text.upper().replace(', ', ',').split(',')
        if len(t) != 2:
            raise BadRequest('You must submit exactly two strings split by comma')
        if (not t[0] and not t[0].strip()) or (not t[1] and not t[1].strip()):
            raise BadRequest('Cannot render empty text')
        clip = VideoFileClip("assets/crab/template.mp4")
        text = TextClip(t[0], fontsize=48, color='white', font='Symbola')
        text2 = TextClip("____________________", fontsize=48, color='white', font='Verdana')\
            .set_position(("center", 210)).set_duration(15.4)
        text = text.set_position(("center", 200)).set_duration(15.4)
        text3 = TextClip(t[1], fontsize=48, color='white', font='Verdana')\
            .set_position(("center", 270)).set_duration(15.4)

        video = CompositeVideoClip([clip, text.crossfadein(1), text2.crossfadein(1), text3.crossfadein(1)]).set_duration(15.4)

        video.write_videofile(name, threads=4, preset='superfast', verbose=False)
        clip.close()
        video.close()
        return send_file(name, mimetype='video/mp4')
