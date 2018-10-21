from io import BytesIO

import requests
from PIL import Image


def get_image(url):
    return Image.open(BytesIO(requests.get(url, stream=True).content))


def get_image_raw(url):
    return requests.get(url, stream=True).content
