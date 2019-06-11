import numpy
from PIL import Image


def find_coeffs(source_coords, target_coords):
    matrix = []
    for s, t in zip(source_coords, target_coords):
        matrix.append([t[0], t[1], 1, 0, 0, 0, -s[0] * t[0], -s[0] * t[1]])
        matrix.append([0, 0, 0, t[0], t[1], 1, -s[1] * t[0], -s[1] * t[1]])
    a = numpy.matrix(matrix, dtype=numpy.float)
    b = numpy.array(source_coords).reshape(8)
    res = numpy.dot(numpy.linalg.inv(a.T * a) * a.T, b)
    return numpy.array(res).reshape(8)


def skew(img, target_cords: list, source_coords: list=None, resolution: int=1024):
    # [(top_left), (top_right), (bottom_right), (bottom_left)]
    if source_coords:
        coeffs = find_coeffs(source_coords, target_cords)
    else:
        coeffs = find_coeffs([(0, 0), (img.width, 0), (img.width, img.height), (0, img.height)], target_cords)
    return img.transform((resolution, resolution), Image.PERSPECTIVE, coeffs,
                          Image.BICUBIC)


