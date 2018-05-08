from io import BytesIO

import requests


def get_image(url):
    return BytesIO(requests.get(url, stream=True).content)
