from io import BytesIO

from PIL import ImageDraw
from flask import send_file

from utils import http
from utils.endpoint import Endpoint, setup


@setup
class Meme(Endpoint):
    params = ['avatar0', 'text']

    def generate(self, avatars, text, usernames):
        img = http.get_image(avatars[0]).convert('RGB')
        font = self.assets.get_font('assets/fonts/impact.ttf', size=48, )
        # parse top and bottom text
        try:
            top_text, bottom_text = text.replace(', ', ',').split(',')
        except ValueError:
            top_text, bottom_text = 'TOP TEXT,BOTTOM TEXT'.split(',')
        draw = ImageDraw.Draw(img)

        def draw_text_with_outline(text, x, y):
            draw.text((x - 2, y - 2), text, (0, 0, 0), font=font)
            draw.text((x + 2, y - 2), text, (0, 0, 0), font=font)
            draw.text((x + 2, y + 2), text, (0, 0, 0), font=font)
            draw.text((x - 2, y + 2), text, (0, 0, 0), font=font)
            draw.text((x, y), text, (255, 255, 255), font=font)
            return

        def draw_text(string, pos):
            string = string.upper()
            w, h = draw.textsize(string, font)  # measure the size the text will take

            line_count = 1
            if w > img.width:
                line_count = int(round((w / img.width) + 1))

            lines = []
            if line_count > 1:

                last_cut = 0
                is_last = False
                for i in range(0, line_count):
                    if last_cut == 0:
                        cut = int((len(string) / line_count) * i)
                    else:
                        cut = int(last_cut)

                    if i < line_count - 1:
                        next_cut = int((len(string) / line_count) * (i + 1))
                    else:
                        next_cut = len(string)
                        is_last = True

                    # make sure we don't cut words in half
                    if not next_cut == len(text) or not text[next_cut] == " ":
                        try:
                            while string[next_cut] != " ":
                                next_cut += 1
                        except IndexError:
                            next_cut = next_cut - 1

                    line = string[cut:next_cut].strip()

                    # is line still fitting ?
                    w, h = draw.textsize(line, font)
                    if not is_last and w > img.width:
                        next_cut -= 1
                        while string[next_cut] != " ":
                            next_cut -= 1

                    last_cut = next_cut
                    lines.append(string[cut:next_cut + 1].strip())

            else:
                lines.append(string)

            last_y = -h
            if pos == "bottom":
                last_y = img.height - h * (line_count + 1) - 10

            for i in range(0, line_count):
                w, h = draw.textsize(lines[i], font)
                x = img.width / 2 - w / 2
                y = last_y + h
                draw_text_with_outline(lines[i], x, y)
                last_y = y

        draw_text(top_text, "top")
        draw_text(bottom_text, "bottom")

        b = BytesIO()
        img.save(b, format='jpeg')
        b.seek(0)
        return send_file(b, mimetype='image/jpeg')
