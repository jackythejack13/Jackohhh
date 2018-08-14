from discord.ext import commands
import json
import discord
from datetime import datetime
import pytz


class Pokemon:
    def __init__(self, bot):
        self.bot = bot
        file = open('cogs/config/pokemon.json', 'rb')
        self.pokestuff = json.loads(file.read())
        file.close()

    @staticmethod
    async def get_stuff_by_type(poke_type):
        if poke_type.lower() == 'normal':
            return [0xd8d8d8, 'https://imgur.com/dewnEma.png']
        if poke_type.lower() == 'ghost':
            return [0x800080, 'https://imgur.com/ejqmbEG.png']
        if poke_type.lower() == 'fighting':
            return [0xaa0000, 'https://imgur.com/MI7gdO1.png']
        if poke_type.lower() == 'bug':
            return [0x80ff00, 'https://imgur.com/SmN3gsA.png']
        if poke_type.lower() == 'dragon':
            return [0x5500ff, 'https://imgur.com/A7kSWAz.png']
        if poke_type.lower() == 'fairy':
            return [0xff80ff, 'https://imgur.com/GknXKpc.png']
        if poke_type.lower() == 'psychic':
            return [0xff00ff, 'https://imgur.com/Jxf0nuU.png']
        if poke_type.lower() == 'dark':
            return [0x400000, 'https://imgur.com/SmN3gsA.png']
        if poke_type.lower() == 'ice':
            return [0x00ffff, 'https://imgur.com/2cY5wzd.png']
        if poke_type.lower() == 'rock':
            return [0x7d5200, 'https://imgur.com/Zj5DQID.png']
        if poke_type.lower() == 'flying':
            return [0x80ffff, 'https://imgur.com/19ckg9I.png']
        if poke_type.lower() == 'ground':
            return [0x9c550e, 'https://imgur.com/sDjw0MO.png']
        if poke_type.lower() == 'grass':
            return [0x00ff00, 'https://imgur.com/K6wMjdP.png']
        if poke_type.lower() == 'electric':
            return [0xffff00, 'https://imgur.com/1NivtAB.png']
        if poke_type.lower() == 'fire':
            return [0xff8000, 'https://imgur.com/vHJxXMy.png']
        if poke_type.lower() == 'water':
            return [0x0000ff, 'https://imgur.com/YgV6sR7.png']
        if poke_type.lower() == 'steel':
            return [0xc0c0c0, 'https://imgur.com/P48ISPL.png']
        if poke_type.lower() == 'poison':
            return [0xc600c6, 'https://imgur.com/F1UK9uZ.png']

    @commands.command(usage="pokemon <pokemon name>", aliases=['poke', 'pk'])
    async def pokemon(self, ctx, *, pokemon):
        poke = pokemon.title().replace(' ', '_')
        for name in self.pokestuff.keys():
            if name != poke:
                continue
            pokemon = self.pokestuff[name]
            poke_id = pokemon['species']
            kind = pokemon['kind']
            try:
                types = '{}/{}'.format(pokemon['type1'], pokemon['type2'])
            except KeyError:
                types = pokemon['type1']
            try:
                ability = '{}, {}, {} (H)'.format(pokemon['ability1'].replace('_', ' '),
                                                  pokemon['ability2'].replace('_', ' '),
                                                  pokemon['hiddenability'].replace('_', ' '))
            except KeyError:
                try:
                    ability = '{}, {}(H)'.format(pokemon['ability1'].replace('_', ' '),
                                                 pokemon['hiddenability'].replace('_', ' '))
                except KeyError:
                    ability = pokemon['ability1'].replace('_', ' ')
            dex = pokemon['desc']
            gender = f"{pokemon['genderratio']} Female" if pokemon['genderratio'] != 'Genderless' else 'Genderless'
            height = pokemon['height']
            weight = pokemon['weight']
            stats = '{} HP, {} Attack, {} Defense, {} Sp Attack, {} Sp Defense, {} Speed'.format(pokemon['stats'][0],
                                                                                                 pokemon['stats'][1],
                                                                                                 pokemon['stats'][2],
                                                                                                 pokemon['stats'][3],
                                                                                                 pokemon['stats'][4],
                                                                                                 pokemon['stats'][5], )
            try:
                evo = pokemon['evolutions'][0]
            except KeyError:
                evo = 'Does not evolve.'
            try:
                prepreicon = pokemon['type2'] if pokemon['type1'] == 'Normal' else pokemon['type1']
            except KeyError:
                prepreicon = pokemon['type1']
            preicon = await Pokemon.get_stuff_by_type(prepreicon)
            icon = preicon[1]
            img = 'http://play.pokemonshowdown.com/sprites/xyani/{}.gif'.format(poke.replace('_', '').lower())
            if poke.startswith('Alolan'):
                img = 'http://play.pokemonshowdown.com/sprites/xyani/{}-alola.gif'.format(
                    poke.replace('_', '').replace('Alolan', '').lower())
            color = preicon[0]
            embed = discord.Embed(color=color)
            embed.set_author(name="(#{0}) {1}".format(poke_id, poke.replace('_', ' ')), icon_url="{}".format(icon))
            embed.set_thumbnail(url="{}".format(img))
            embed.add_field(name='Species', value='{}'.format(kind), inline=True)
            embed.add_field(name='Types', value='{}'.format(types), inline=True)
            embed.add_field(name='Abilities', value='{}'.format(ability), inline=False)
            embed.add_field(name='Gender Rate', value='{}'.format(gender), inline=True)
            embed.add_field(name='Height & Weight', value='{} / {}'.format(height, weight), inline=True)
            embed.add_field(name='Dex Entry', value='{}'.format(dex), inline=True)
            embed.add_field(name='Evolution Line', value='{}'.format(evo), inline=True)
            embed.add_field(name='Base Stats', value='{}'.format(stats), inline=True)
            embed.set_footer(text="{} | {}".format(str(ctx.message.author),
                                                   datetime.now(pytz.timezone('Pacific/Auckland')).strftime(
                                                       "%I:%M%p %m/%d/%Y")))
            await ctx.send(embed=embed)
            return
        await ctx.send(f'`{pokemon}` was not found in my database.')


def setup(bot):
    bot.add_cog(Pokemon(bot))
