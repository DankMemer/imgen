from io import BytesIO

from PIL import Image, ImageDraw
from flask import send_file
from utils import http

from utils.endpoint import Endpoint, setup
from utils.textutils import wrap


@setup
class Profile(Endpoint):
    """Note: This endpoint is only accessible to Dank Memer. Do NOT implement this!"""
    params = ['avatar1', 'username1', 'image', 'bio', 'title', 'level', 'xp', 'total_xp', 'color', 'bank', 'wallet', 'inventory', 'prestige', 'active_effects', 'command', 'streak', 'multiplier']

    def generate(self, avatars, text, usernames, kwargs):
        font = self.assets.get_font('assets/fonts/MontserratBold.ttf', size=30, )
        font2 = self.assets.get_font('assets/fonts/Montserrat.ttf', size=22, )
        font3 = self.assets.get_font('assets/fonts/MontserratBold.ttf', size=30, )
        test = Image.new('L', (1, 1))
        test_draw = ImageDraw.Draw(test)

        active_effects = kwargs.get('active_effects', None)
        total_h = 0
        if active_effects:
            effects = active_effects.split('-')
            for i in effects:
                w, h = test_draw.textsize(wrap(font2, i, 200), font2)
                total_h = total_h + h

        base = Image.new('RGBA', (600, 600 + total_h + 32), '#2C2F33')
        image = http.get_image(kwargs.get('image', 'https://i.imgur.com/G68osEq.jpg')).resize((600, 260), Image.LANCZOS).convert('RGB')
        base.paste(image, (0, 0))
        avatar = http.get_image(avatars[0]).resize((96, 96), Image.LANCZOS).convert('RGB')

        avatar_pos = int(base.width / 2 - avatar.width / 2), int(image.height - avatar.height / 2) - 20

        bio = kwargs.get('bio', None)
        if bio:
            if len(bio) > 40:
                bio = bio[:40] + '...'

        title = kwargs.get('title', None)
        xp = kwargs.get('xp', '0')
        level = int(int(xp) / 100)
        next_xp = (int(level) + 1) * 100

        color = kwargs.get('color', 'cyan')

        xp_dim = int((int(xp) - level * 100) / (next_xp - (level*100)) * 200) + 1, 5

        bank = "{:,}".format(int(kwargs.get('bank', '0')))
        wallet = "{:,}".format(int(kwargs.get('wallet', '0')))

        prestige = kwargs.get('prestige', None)
        inventory = kwargs.get('inventory', '0 items worth 0 coins')

        command = kwargs.get('command', 'No favorite command')
        streak = kwargs.get('streak', '0')
        multiplier = kwargs.get('multiplier', '0')

        line = Image.new('RGBA', (base.width, 2), '#1a1c1e')
        line2 = Image.new('RGBA', (base.width, 2), '#1f2123')
        line3 = Image.new('RGBA', (base.width, 2), '#232528')
        line4 = Image.new('RGBA', (base.width, 2), '#272a2d')
        line5 = Image.new('RGBA', (base.width, 2), '#2C2F33')

        bigsize = (avatar.size[0] * 3, avatar.size[1] * 3)
        mask = Image.new('L', bigsize, 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0) + bigsize, fill=255)
        mask = mask.resize(avatar.size, Image.ANTIALIAS)
        avatar.putalpha(mask)

        avatar_line = Image.new('RGBA', (1024, 1024), (255, 0, 0, 0))
        dr = ImageDraw.Draw(avatar_line)
        dr.ellipse((0, 0, 1024, 1024), fill='white')

        avatar_line = avatar_line.resize((104, 104), resample=Image.LANCZOS)

        # Reused code from youtube endpoint to generate rounded avatar
        base.paste(line, (0, image.height))
        base.paste(line2, (0, image.height + 2))
        base.paste(line3, (0, image.height + 4))
        base.paste(line4, (0, image.height + 6))
        base.paste(line5, (0, image.height + 8))

        # Gradient under image

        base.paste(avatar_line, (avatar_pos[0] - 4, avatar_pos[1] - 4), avatar_line)
        base.paste(avatar, avatar_pos, avatar)  # Calculate center with banner bottom - 64 and image width - 64

        if prestige:
            icon = Image.open(self.assets.get(f'assets/profile/prestige/{prestige}.png'))
            base.paste(icon, (avatar_pos[0] + 64, avatar_pos[1] - 16), icon)

        draw = ImageDraw.Draw(base)

        name_text = draw.textsize(usernames[0], font=font)
        name_box = Image.new('RGBA', (name_text[0] + 30, name_text[1] + 30), (0, 0, 0, 230))
        base.paste(name_box, (0, 20), name_box)
        draw.text((10, 34), usernames[0], font=font, fill=(255, 255, 255, 255))
        if bio:
            bio_text = draw.textsize(bio, font=font2)
            bio_box = Image.new('RGBA', (bio_text[0] + 20, bio_text[1] + 20), (0, 0, 0, 230))
            base.paste(bio_box, (0, 20 + name_box.height + 20), bio_box)
            draw.text((10, bio_box.height + name_box.height + 4), bio, font=font2, fill=(255, 255, 255, 255))
        if not bio:
            bio_box = Image.new('RGBA', (20, 20), (0, 0, 0, 230))

        if title:
            title_text = draw.textsize(title, font=font2)
            title_box = Image.new('RGBA', (title_text[0] + 20, title_text[1] + 20), (0, 0, 0, 230))
            base.paste(title_box, (0, 20 + name_box.height + bio_box.height + 60), title_box)
            draw.text((10, bio_box.height + name_box.height + title_box.height + 46), title, font=font2, fill=(0, 256, 0))

        draw.text((15, 290), 'Level', font=font3)

        draw.line((15, base.height - 95, 585, base.height - 95), width=1, fill='white')
        draw.text((15, base.height - 85), f'FAVORITE COMMAND: {command}\nSTREAK: {streak} days\nMULTIPLIER: {multiplier}%', font=font2)

        current_level_size = draw.textsize(str(level), font=font2)
        draw.text((15, 340), str(level), font=font2)
        draw.text((15 + current_level_size[0] + 200 + 15, 340), str(int(level) + 1), font=font2)
        draw.text((15, 365), f'{xp} XP - {((level + 1) * 100) - int(xp)} remaining', font=font2)

        draw.text((370, 290), 'Coins', font=font3)
        draw.text((370, 340), f'Wallet: {wallet}', font=font2)
        draw.text((370, 365), f'Bank: {bank}', font=font2)

        draw.text((15, 410), 'Inventory', font=font3)
        draw.text((15, 460), wrap(font2, inventory, 300), font=font2)

        draw.text((370, 410), 'Active Items', font=font3)
        if active_effects:
            possible_effects = ['alcohol', 'cupidsbigtoe', 'fakeid', 'padlock', 'sand', 'santashat', 'spinner', 'tidepod', 'landmine']
            height = 0
            for i in effects:
                for j in possible_effects:
                    if i.startswith(f':{j}:'):
                        effect = i.replace(f':{j}:', '')
                        effect_icon = Image.open(self.assets.get(f'assets/profile/activeitems/{j}.png')).resize((32, 32), Image.LANCZOS)
                        base.paste(effect_icon, (365, 455 + height), effect_icon)
                        w, h = draw.textsize(wrap(font2, effect, 170), font2)
                        draw.text((402, 460 + height), wrap(font2, effect, 170), font=font2)
                        height = height + 15 + h
        else:
            draw.text((370, 460), 'No active items', font=font2)

        # LEVEL BAR SHOULD BE DRAWN LAST. THAT MEANS YOU DEVOXIN. DON'T TOUCH

        level_bar = Image.new('RGBA', (200, 5), color='grey')
        if color == 'gay':
            next_bar = Image.new('RGBA', xp_dim, color='red')
            colours = [(255, 0, 0), (255, 127, 0), (255, 255, 0), (0, 255, 255), (0, 0, 255), (63, 0, 255), (127, 0, 255)]
            next_bar_draw = ImageDraw.Draw(next_bar)
            count = 0
            count2 = 0
            for i in range(int(next_bar.width)):
                if count == len(colours):
                    count = 0
                choice = colours[count]
                for j in range(5):
                    next_bar_draw.point((i, j), fill=choice)
                count2 = count2 + 1
                if count2 == 4:
                    count2 = 0
                    count = count + 1

        else:
            next_bar = Image.new('RGBA', xp_dim, color=color)
        circle = Image.new('L', (20, 20), 0)
        circle2 = Image.new('L', (20, 20), 0)
        draw = ImageDraw.Draw(circle)
        draw2 = ImageDraw.Draw(circle2)
        draw.ellipse((0, 0, 20, 20), fill=255)
        draw2.ellipse((0, 0, 20, 20), fill=255)
        alpha = Image.new('L', level_bar.size, 255)
        alpha2 = Image.new('L', next_bar.size, 255)
        w, h = level_bar.size
        w2, h2 = next_bar.size
        rad = 1
        alpha.paste(circle.crop((rad, 0, rad * 2, rad)), (w - rad, 0))
        alpha.paste(circle.crop((rad, rad, rad * 2, rad * 2)), (w - rad, h - rad))
        level_bar.putalpha(alpha)
        alpha2.paste(circle.crop((0, 0, rad, rad)), (0, 0))
        alpha2.paste(circle.crop((0, rad, rad, rad * 2)), (0, h2 - rad))
        next_bar.putalpha(alpha2)

        base.paste(level_bar, (15 + current_level_size[0] + 10, 340 + int(current_level_size[1] / 2)), level_bar)
        base.paste(next_bar, (15 + current_level_size[0] + 9, 340 + int(current_level_size[1] / 2)), next_bar)

        b = BytesIO()
        base.save(b, format='png')
        b.seek(0)
        return send_file(b, mimetype='image/png')
