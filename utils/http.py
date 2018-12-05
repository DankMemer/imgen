import json
from io import BytesIO

import requests
from PIL import Image

config = json.load(open('config.json'))
MAX_FILE_SIZE = config.get('max_file_size', 5000000)  # in bytes


def get(url, **kwargs):
    if 'proxy_url' in config:
        res = requests.get(config['proxy_url'], params={'url': url}, **kwargs)
    else:
        res = requests.get(url, **kwargs)

    if 'content-length' not in res.headers:
        raise KeyError(f'{url} is missing `content-length` header')

    if int(res.headers.get('content-length', 0)) > MAX_FILE_SIZE:
        raise OverflowError(f'content-length may not exceed {MAX_FILE_SIZE} bytes')

    return res


def get_content_raw(url, **kwargs):
    return get(url, stream=True, **kwargs).content


def get_image(url, **kwargs):
    try:
        raw = get_content_raw(url, **kwargs)
        return Image.open(BytesIO(raw))
    except OSError:
        raise TypeError('An invalid image was provided! Check the URL and try again.')
