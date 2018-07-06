from io import BytesIO

from flask import send_file

from utils.endpoint import Endpoint


class Brazzers(Endpoint):
    def generate(self, avatars, text, usernames):
        ((avatar,), base) = self.setup(
            avatars,
            ((500, 500), (300, 150)),
            'brazzers'
        )

        # avatar is technically the base
        avatar.paste(base, (200, 390), base)

        b = BytesIO()
        avatar.save(b, format='png')
        b.seek(0)
        return send_file(b, mimetype='image/png')


def setup():
    return Brazzers()
