from io import BytesIO

from flask import send_file
from PIL import Image, ImageDraw, ImageFont, ImageEnhance

from utils import http
from utils.endpoint import Endpoint
from utils.textutils import wrap


class Unpopular(Endpoint):
    def generate(self, avatars, text, usernames):
        avatar = http.get_image(avatars[0]).resize((666, 666)).convert('RGBA')
        base = Image.open('assets/unpopular/unpopular.png').convert('RGBA')
        font = ImageFont.truetype(font='assets/fonts/semibold.woff', size=100)
        reticle = Image.open('assets/unpopular/reticle.png').convert('RGBA')
        temp = Image.new('RGBA', (1200, 800), color=(0, 0, 0, 0))
        avatar_square = Image.new(mode='RGBA', size=(360, 270), color=(0, 0, 0, 0))
        avatar_mono = avatar.resize((300, 310)).rotate(16, expand=1).convert('1')
        avatar_darkened = ImageEnhance.Brightness(avatar_mono.convert('RGB')).enhance(0.5)
        avatar_square.paste(avatar_darkened, (0, 0), avatar_mono)

        bigsize = (avatar.size[0] * 3, avatar.size[1] * 3)
        mask = Image.new('L', bigsize, 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0) + bigsize, fill=255)
        mask = mask.resize(avatar.size, Image.ANTIALIAS)
        avatar.putalpha(mask)

        base.paste(avatar, (1169, 1169), avatar)
        face = avatar.resize((368, 368))
        base.paste(face, (140, 250), face)
        base.paste(reticle, (1086, 1086), reticle)
        base.paste(avatar_square, (-20, 1670), avatar_square)
        canv = ImageDraw.Draw(temp)
        wrapped = wrap(font, text, 1150)
        canv.text((0, 0), wrapped, font=font, fill='Black')
        w = temp.rotate(1, expand=1)
        base.paste(w, (620, 280), w)

        b = BytesIO()
        base.save(b, format='png')
        b.seek(0)
        return send_file(b, mimetype='image/png')


def setup():
    return Unpopular()
