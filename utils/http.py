from io import BytesIO

import requests
from PIL import Image
import json

config = json.load(open('config.json'))


def get_image(url):
    try:
        if 'proxy_url' in config:
            return Image.open(BytesIO(requests.get(config['proxy_url'] + '?url=' + url,
                                                   stream=True).content))
        else:
            return Image.open(BytesIO(requests.get(url, stream=True).content))
    except OSError:
        raise TypeError('An invalid image was provided! Check the URL and try again.')


def get_image_raw(url):
    if 'proxy_url' in config:
        return requests.get(config['proxy_url'] + '?url=' + url, stream=True).content
    else:
        return requests.get(url, stream=True).content
