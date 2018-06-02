import subprocess

from utils.http import get_image_raw


def convert(image: str, args: list, output_format: str):
    img_bytes = get_image_raw(image)
    args = ['gm', 'convert', '-'] + args + ['{}:-'.format(output_format)]

    proc = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
    stdout, stderr = proc.communicate(img_bytes)
    return stdout
