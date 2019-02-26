from flask import jsonify

from utils.endpoint import Endpoint, setup
from random import choice


@setup
class YoMomma(Endpoint):
    """
    This endpoint only returns a yo momma joke. No parameters are required.
    """
    params = []

    def generate(self, avatars, text, usernames, kwargs):
        choices = ['Yo momma so fat when she walked past the TV I missed three episodes',
                   'Yo momma so stupid she stuck a battery up her ass and said "I GOT THE POWER"',
                   'Yo momma so dumb, when y\'all were driving to Disneyland, she saw a sign that said "Disneyland left", so she went home',
                   'Yo momma so fat she needs cheat codes for Wii Fit',
                   'Yo momma so fat when she went to KFC and they asker her what size of bucket, she said "The one on the roof"',
                   'Yo momma so fat, I took a picture of her last Christmas and it\'s still printing',
                   'Yo momma so fat and old when God said "Let there be light" he asked your momma to step out of the way',
                   'Yo momma so fat when she stept out in a yellow jacket people yell TAXI',
                   'Yo momma so fat I tried driving around her and I ran out of gas',
                   'Yo momma so fat it took Thanos two snaps to kill her',
                   'Yo momma so fat she sued Nintendo for guessing her weight',
                   'Yo momma so dumb, she tripped over WiFi',
                   'Yo momma so fat she has two watches, one for each timezone',
                   'Yo momma so fat she left the house in high heels and came back in flip flops',
                   'Yo momma so fat her blood type is Nutella',
                   'Yo momma so fat she uses Google Earth to take a selfie',
                   'Yo momma so fat even Dora could not explore her',
                   'Yo momma so fat she jumped in the air and got stuck',
                   'Yo momma so fat that when we were born, she gave the hospital stretch marks',
                   'Yo momma so fat she wears a sock on each toe',
                   'Yo momma so fat the army uses her underwear as parachutes',
                   'Yo momma so fat her patronus is a cake',
                   'Yo momma so fat when she tripped over on 4th Ave, she landed on 12th',
                   'Yo momma so fat the only way she burns calories is when her food is on fire',
                   'Yo momma so fat she won all 75 Hunger Games',
                   'Yo momma so fat when she steps on a scale it says "One at a time please"',
                   'Yo momma so fat she got her own area code',
                   'Yo momma so fat even Kirby can'' eat her',
                   'Yo momma so fat when she went to the beach Greenpeace threw her into the ocean',
                   'Yo momma so fat a vampire bit her and got Type 2 diabetes',
                   'Yo momma so fat she uses butter for her chapstick',
                   'Yo momma so fat when she walks backwards she beeps',
                   'Yo momma so fat she puts mayo on her diet pills']
        return jsonify({"text": choice(choices)})
