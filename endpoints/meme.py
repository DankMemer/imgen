from io import BytesIO

from PIL import ImageDraw, Image
from flask import send_file

from utils import http
from utils.endpoint import Endpoint, setup
from utils.textutils import wrap, render_text_with_emoji


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
    params = ['avatar0', 'top_text', 'bottom_text', 'color', 'font']

    def generate(self, avatars, text, usernames, kwargs):  # pylint: disable=R0915
        img = http.get_image(avatars[0]).convert('RGBA')
        factor = int(img.height / 10)
        font = self.assets.get_font(f'assets/fonts/{kwargs.get("font", "impact")}.ttf', size=factor)
        draw = ImageDraw.Draw(img)
        color = kwargs.get('color', 'white')

        def draw_text_with_outline(string, x, y):
            x = int(x)
            y = int(y)
            render_text_with_emoji(img, draw, (x - 2, y - 2), string, font=font, fill=(0, 0, 0))
            render_text_with_emoji(img, draw, (x + 2, y - 2), string, font=font, fill=(0, 0, 0))
            render_text_with_emoji(img, draw, (x + 2, y + 2), string, font=font, fill=(0, 0, 0))
            render_text_with_emoji(img, draw, (x - 2, y + 2), string, font=font, fill=(0, 0, 0))
            render_text_with_emoji(img, draw, (x, y), string, font=font, fill=color)

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

        if kwargs.get('altstyle', 'null').lower() == 'true':
            text_font = self.assets.get_font(f'assets/fonts/{kwargs.get("font", "arial")}.ttf', size=24)
            text = wrap(text_font, kwargs.get('top_text', 'TOP TEXT'), img.width)
            text_img = Image.new('RGB', (img.width, 10000), 'white')
            text_draw = ImageDraw.Draw(text_img)
            text_size = text_draw.textsize(text, text_font)
            new_image = Image.new('RGB', (img.width, img.height + text_size[1] + 10), 'white')
            new_image.paste(img, (0, text_size[1] + 10))
            new_draw = ImageDraw.Draw(new_image)
            new_draw.text((0, 0), text, kwargs.get('color', 'black'), text_font)
            img = new_image

        else:
            draw_text(kwargs.get('top_text', 'TOP TEXT'), "top")
            draw_text(kwargs.get('bottom_text', 'BOTTOM TEXT'), "bottom")

        b = BytesIO()
        img.save(b, format='png')
        b.seek(0)
        return send_file(b, mimetype='image/png')
