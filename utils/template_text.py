from PIL import ImageDraw

from utils.exceptions import BadRequest


def _bounds(draw, value, font):
    if hasattr(draw, 'textbbox'):
        return draw.textbbox((0, 0), value, font=font)
    width, height = draw.textsize(value, font=font)
    return 0, 0, width, height


def _width(draw, value, font):
    left, _, right, _ = _bounds(draw, value, font)
    return right - left


def _lines(draw, value, font, width):
    result = []
    for paragraph in value.split('\n'):
        current = ''
        for word in paragraph.split():
            candidate = word if not current else current + ' ' + word
            if _width(draw, candidate, font) <= width:
                current = candidate
                continue
            if current:
                result.append(current)
                current = ''
            for char in word:
                if current and _width(draw, current + char, font) > width:
                    result.append(current)
                    current = ''
                current += char
        result.append(current)
    return result


def draw_fitted_text(image, value, box, get_font, maximum, minimum=12, fill='black', max_lines=None):
    if not isinstance(value, str) or not value.strip():
        raise BadRequest('Provide non-empty text.')

    draw = ImageDraw.Draw(image)
    left, top, right, bottom = box
    width = right - left
    height = bottom - top
    value = value.strip()

    for size in range(maximum, minimum - 1, -1):
        font = get_font(size)
        lines = _lines(draw, value, font, width)
        ascent, descent = font.getmetrics()
        line_height = ascent + descent
        if max_lines is not None and len(lines) > max_lines:
            continue
        if len(lines) * line_height > height:
            continue

        y = top + (height - len(lines) * line_height) / 2
        for line in lines:
            bounds = _bounds(draw, line, font)
            text_width = bounds[2] - bounds[0]
            x = left + (width - text_width) / 2 - bounds[0]
            draw.text((x, y), line, font=font, fill=fill)
            y += line_height
        return

    raise BadRequest('Text is too long for this template.')
