def wrap(font, text, line_width):
    characters = list(text)

    lines = []
    line = ''

    while characters:
        char = characters.pop(0)
        newline = line + char

        w, h = font.getsize(newline)

        if w > line_width:
            lines.append(line)
            line = char
        else:
            line = newline

    if line:
        lines.append(line)

    return '\n'.join(lines)

# TODO: Fix words having characters newlined if overfill
