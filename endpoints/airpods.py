from io import BytesIO

from PIL import Image
from flask import send_file

from utils import http
from utils.endpoint import Endpoint, setup
import numpy

@setup
class Airpods(Endpoint):
    params = ['avatar0']

    def generate(self, avatars, text, usernames, kwargs):
        white = Image.new('RGBA', (2048, 1364), 0x00000000)
        base = Image.open(self.assets.get('assets/airpods/airpods.png'))
        img1 = http.get_image(avatars[0]).convert('RGBA').resize((512, 512), Image.LANCZOS)
        coeffs = find_coeffs(
            [(0, 0), (512, 0), (512, 512), (0, 512)],
            [(476, 484), (781, 379), (956, 807), (668, 943)])

        img1 = img1.transform((1024, 1024), Image.PERSPECTIVE, coeffs,
                      Image.BICUBIC)
        # img1 = img1.rotate(21.5, expand=True, resample=Image.BICUBIC)
        white.paste(img1, (0, 0), img1)
        white.paste(base, (0, 0), base)
        white = white.convert('RGBA')

        b = BytesIO()
        white.save(b, format='png')
        b.seek(0)
        return send_file(b, mimetype='image/png')


def find_coeffs(source_coords, target_coords):
    matrix = []
    for s, t in zip(source_coords, target_coords):
        matrix.append([t[0], t[1], 1, 0, 0, 0, -s[0] * t[0], -s[0] * t[1]])
        matrix.append([0, 0, 0, t[0], t[1], 1, -s[1] * t[0], -s[1] * t[1]])
    A = numpy.matrix(matrix, dtype=numpy.float)
    B = numpy.array(source_coords).reshape(8)
    res = numpy.dot(numpy.linalg.inv(A.T * A) * A.T, B)
    return numpy.array(res).reshape(8)
