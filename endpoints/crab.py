import uuid
import os
from flask import send_file, after_this_request

from utils.endpoint import Endpoint, setup

from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip


@setup
class Crab(Endpoint):
    """his endpoint returns an MP4 file. Make sure your application knows how to handle this format."""
    params = ['text']

    def generate(self, avatars, text, usernames, kwargs):
        @after_this_request
        def remove(response):
            os.remove(name)
            return response

        t = text.upper().replace(', ', ',').split(',')
        clip = VideoFileClip("assets/crab/template.mp4")

        text = TextClip(t[0], fontsize=48, color='white', font='Verdana')
        text2 = TextClip("____________________", fontsize=48, color='white', font='Verdana')
        text = text.set_position(("center", 200)).set_duration(15)
        text2 = text2.set_position(("center", 210)).set_duration(15)
        text3 = TextClip(t[1], fontsize=48, color='white', font='Verdana')
        text3 = text3.set_position(("center", 270)).set_duration(15)

        video = CompositeVideoClip([clip, text, text2, text3]).set_duration(15)

        name = str(uuid.uuid4().hex) + '.mp4'
        video.write_videofile(name, threads=4, preset='superfast')

        return send_file(name, mimetype='video/mp4')


