from io import BytesIO

import requests
from PIL import Image


def get_image(url):
    try:
        return Image.open(BytesIO(requests.get(url, stream=True).content))
    except OSError:
        raise TypeError('An invalid image was provided! Check the URL and try again.')


def get_image_raw(url):
    return requests.get(url, stream=True).content
