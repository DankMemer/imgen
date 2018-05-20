from io import BytesIO

import requests


def get_image(url):
    return BytesIO(requests.get(url, stream=True).content)


def get_image_raw(url):
    return requests.get(url, stream=True).content
