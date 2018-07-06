from io import BytesIO

from flask import send_file

from utils.endpoint import Endpoint


class Slap(Endpoint):
    def generate(self, avatars, text, usernames):
        ((avatar, avatar2), base) = self.setup(
            avatars,
            ((220, 220), (200, 200), (1000, 500)),
            "batslap",
            file_format="jpg"
        )

        base.paste(avatar2, (580, 260), avatar2)
        base.paste(avatar, (350, 70), avatar)

        b = BytesIO()
        base.save(b, format="png")
        b.seek(0)
        return send_file(b, mimetype="image/png")


def setup():
    return Slap()
