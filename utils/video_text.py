import os
import subprocess
from functools import lru_cache

from PIL import Image, ImageDraw, ImageFont


@lru_cache(maxsize=8)
def _font(name, size):
    path = os.path.join('assets', 'fonts', name.lower() + '.ttf')
    if not os.path.isfile(path):
        try:
            path = subprocess.check_output(
                ['fc-match', '-f', '%{file}', name], stderr=subprocess.DEVNULL
            ).decode('utf-8').strip()
        except (OSError, subprocess.CalledProcessError):
            path = ''
    if not os.path.isfile(path):
        path = os.path.join('assets', 'fonts', 'verdana.ttf')
    return ImageFont.truetype(path, size)


def _bounds(draw, value, font, stroke_width):
    value = value or ' '
    if hasattr(draw, 'textbbox'):
        return draw.textbbox((0, 0), value, font=font, stroke_width=stroke_width)
    width, height = draw.textsize(value, font=font, stroke_width=stroke_width)
    return 0, 0, width, height


def _wrap(value, width, draw, font, stroke_width):
    if width is None:
        return value.split('\n')

    lines = []
    for paragraph in value.split('\n'):
        current = ''
        for char in paragraph:
            candidate = current + char
            left, _, right, _ = _bounds(draw, candidate, font, stroke_width)
            if current and right - left > width:
                split = current.rfind(' ')
                if split > 0:
                    lines.append(current[:split])
                    current = current[split + 1:] + char
                else:
                    lines.append(current)
                    current = char
            else:
                current = candidate
        lines.append(current)
    return lines


def render_video_text(value, font_name, font_size, color, width=None, background=None, stroke_width=0):
    font = _font(font_name, font_size)
    draw = ImageDraw.Draw(Image.new('RGBA', (1, 1)))
    lines = _wrap(value, width, draw, font, stroke_width)
    ascent, descent = font.getmetrics()
    line_height = ascent + descent
    if width is None:
        width = 1
        for line in lines:
            left, _, right, _ = _bounds(draw, line, font, stroke_width)
            width = max(width, right - min(0, left))

    image = Image.new('RGBA', (max(1, width), max(1, line_height * len(lines))), background or (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    for index, line in enumerate(lines):
        left, _, _, _ = _bounds(draw, line, font, stroke_width)
        draw.text(
            (max(0, -left), index * line_height),
            line,
            font=font,
            fill=color,
            stroke_width=stroke_width,
            stroke_fill=color,
        )
    return image
