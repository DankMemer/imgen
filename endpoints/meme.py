from io import BytesIO

from PIL import ImageDraw
from flask import send_file

from utils import http
from utils.endpoint import Endpoint, setup


@setup
class Meme(Endpoint):
    """
    This endpoint works a bit differently from the other endpoints.
    This endpoint takes in top_text and bottom_text parameters instead of text.
    It also supports color and font parameters.
    Fonts supported are: arial, arimobold, impact, robotomedium, robotoregular, sans, segoeuireg, tahoma and verdana.
    Colors can be defined with HEX codes or web colors, e.g. black, white, orange etc. Try your luck ;)
    The default is Impact in white
    """
    params = ['avatar0']

    def generate(self, avatars, text, usernames, kwargs):  # pylint: disable=R0915
        img = http.get_image(avatars[0]).convert('RGBA')
        factor = int(img.height / 10)
        font = self.assets.get_font(f'assets/fonts/{kwargs.get("font", "impact")}.ttf', size=factor)
        draw = ImageDraw.Draw(img)
        color = kwargs.get('color', 'white')

        def draw_text_with_outline(string, x, y):
            draw.text((x - 2, y - 2), string, (0, 0, 0), font=font)
            draw.text((x + 2, y - 2), string, (0, 0, 0), font=font)
            draw.text((x + 2, y + 2), string, (0, 0, 0), font=font)
            draw.text((x - 2, y + 2), string, (0, 0, 0), font=font)
            draw.text((x, y), string, color, font=font)

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

        draw_text(kwargs.get('top_text', 'TOP TEXT'), "top")
        draw_text(kwargs.get('bottom_text', 'BOTTOM TEXT'), "bottom")

        b = BytesIO()
        img.save(b, format='png')
        b.seek(0)
        return send_file(b, mimetype='image/png')
