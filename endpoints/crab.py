import uuid
import os
from flask import send_file, after_this_request

from utils.endpoint import Endpoint, setup
from utils.exceptions import BadRequest

from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip



@setup
class Crab(Endpoint):
    """
    This endpoint returns an MP4 file. Make sure your application knows how to handle this format.
    This endpoint has a ratelimit of 1 request per 30 seconds.
    This ratelimit will also apply to all other (future) video based endpoints.
    Erronous requests count against your limit.
    Separate text with a comma.
    """
    params = ['text']

    def generate(self, avatars, text, usernames, kwargs):
        @after_this_request
        def remove(response):
            try:
                os.remove(name)
            except Exception:
                pass
            return response
        t = text.upper().replace(', ', ',').split(',')
        t_1 = t[0]
        t_2 = t[1]
        if (not t_1 and not t_1.strip()) or (not t_2 and not t_2.strip()):
            raise BadRequest('Cannot render empty text')
        clip = VideoFileClip("assets/crab/template.mp4")
        text = TextClip(t_1, fontsize=48, color='white', font='Verdana')
        text2 = TextClip("____________________", fontsize=48, color='white', font='Verdana')
        text = text.set_position(("center", 200)).set_duration(15.4)
        text2 = text2.set_position(("center", 210)).set_duration(15.4)
        text3 = TextClip(t_2, fontsize=48, color='white', font='Verdana')
        text3 = text3.set_position(("center", 270)).set_duration(15.4)

        video = CompositeVideoClip([clip, text.crossfadein(1), text2.crossfadein(1), text3.crossfadein(1)]).set_duration(15.4)

        name = uuid.uuid4().hex + '.mp4'
        video.write_videofile(name, threads=1, preset='superfast', verbose=False, progress_bar=False)

        return send_file(name, mimetype='video/mp4')
