# -*- coding: utf8 -*-

import os
import pytz
import json
import discord
import asyncio
import random
import traceback
import string
import inspect
from datetime import datetime
from discord.ext import commands
from discord.utils import get

accept = input("Gamma.\nA bot made using Python and Discord.py.\n"
               "This bot is maintained by Xua#8831 and "
               "this code belongs to him.\nAny unauthorized "
               "copying of this bot will result in punishment "  
               "as chosen by Xua#8831 himself.\n(NOTE) "
               "If you wish to clone Gamma, please get in contact "
               "with Xua#8831 as soon as possible.\nDo you accept "
               "these terms?\n(y/n) >>> ")

if not accept.lower().startswith('y'):
    import sys
    sys.exit(-1)

(lambda: os.system('clear'))()

desc = """Hi there, I'm Gamma.
I am a bot created and maintained by Xua#8831
Here is a list of commands and modules that are currently running."""
startup_extensions = ['cogs.debug', 'cogs.moderation', 'cogs.youtube', 'cogs.miscellaneous', 'cogs.pokemon',
                      'cogs.customcommands', 'cogs.admin']

file = open('cogs/config/config.json')
config = json.loads(file.read())
file.close()

mode = "Sigma" if config['indev'] else "Gamma"
debug = mode.lower() == "sigma"


#   CHECKS
def is_xua(ctx):
    return ctx.message.author.id == 285915453094756362


def is_server_owner():
    pass

#   CUSTOM


def combine(l, space):
    """Combines a list into a string"""
    n = ''
    for x in l:
        try:
            if space:
                n = f'{n} {x}'
            else:
                n = f'{n}{x}'
        except Exception:
            raise ValueError(f'{x} is not a string!')
    return n


old_print = print

log_string = ""


def print(data, bort=None):
    global log_string
    time = datetime.now(pytz.timezone('Pacific/Auckland')).strftime("%Y-%m-%d: %H:%M:%S")
    to_write = f'[{time}] {data}'
    log_string = f"{log_string}{to_write}\n"
    old_print(to_write)
    if bort:
        bort.log_string = log_string
        

def join(data, member):
    alpha = data.replace('##', f'{member.guild.name}')
    beta = alpha.replace('@@', f'<@{member.id}>')
    charlie = beta.replace('%%', f'{member.name}')
    delta = charlie.replace('&&', f'{member}')
    return delta


class Gamma(commands.Bot):

    def __init__(self):
        self.prefix = config['prefix']
        super().__init__(command_prefix=self.get_pref, description=desc)
        pfile = open('cogs/config/server_data.json')
        self.server_data = json.loads(pfile.read())
        pfile.close()
        self.config = config
        self.muted_roles = []
        self.combine = combine
        self.logstring = log_string
        self.reboot = datetime.now()
        self.logging_channels = {}
        self.welcome_channels = {}
        self.format_join = join
        self.is_server_purging = {}
        self.custom_commands = {}
        self.ignore = []
        self.debug = debug
    
    async def update_prefix(self, guild: discord.Guild, pref):
        # edit servers prefix here
        # noinspection PyBroadException
        try:
            self.server_data[str(guild.id)]['prefix'] = pref
            return "Set prefix to `" + pref + '`'
        except Exception as e:
            await self.get_channel(458771285414117387).send(f"{type(e).__name__}: {e}")
            return "An error occurred and has been reported to **Xua#8831**"
        pass

    def get_pref(self, bot: commands.Bot, message: discord.Message):
        if not bot:
            print('wut')
        try:
            return self.server_data[str(message.guild.id)]['prefix']
        except KeyError:
            return "~" if not debug else "+"

    def run(self):
        self.loop.create_task(self.presence_updater())
        self.loop.create_task(self.hourly_update())
        for extension in startup_extensions:
            try:
                self.load_extension(extension)
            except Exception as e:
                exc: str = '{}: {}'.format(type(e).__name__, e)
                print('Failed to load extension "{}": {}'.format(extension, exc), self)
        super().run(config[f'token{mode}'])
        
    async def _save(self):
        f = open('cogs/config/server_data.json', 'w')
        f.write(json.dumps(self.server_data))
        f.close()
        await (self.get_channel(458771285414117387)).send("Server data was saved.")

    async def daily_update(self):
        await asyncio.sleep(86400)

    async def hourly_update(self):
        await self.wait_until_ready()
        await self._save()
        await asyncio.sleep(3600)
        
    async def minutely_update(self):
        await asyncio.sleep(60)
    
    async def secondly_update(self):
        await asyncio.sleep(1)
        
    async def presence_updater(self):
        await self.wait_until_ready()
        while not self.is_closed():
            time = datetime.now(tz=pytz.timezone("Pacific/Auckland")).strftime("%I:%M%p")
            await self.change_presence(activity=discord.Game(name=f"{self.prefix}help | {time} NZT",
                                                             type=discord.ActivityType.playing),
                                       status=discord.Status.online)
            await asyncio.sleep(20)

    async def get_muted_role(self, guild):
        for role in guild.roles:
            for role2 in self.muted_roles:
                if role2.id == role.id:
                    return role2
        else:
            print(f'No muted role found for guild {guild.name}', self)
            return

    async def on_message(self, message):
        if message.author.bot:
            if not message.content.startswith(self.prefix):
                return
            else:
                await message.add_reaction(get(self.emojis, name="lul"))
                return
        if message.author.id in self.ignore:
            return
        # This entire chunk of code is irrelevant, remind me to delete it
        # It is only here as a reference when i rewrite it.
        if len(message.mentions) > 0:
            for member in message.mentions:
                if member.id == message.guild.me.id:
                    emote = [emote for emote in self.emojis if "ping" in emote.name.lower()]
                    await message.add_reaction(random.choice(emote))
                    break
        if message.mention_everyone:
            for emote in self.get_guild(455889701992398854).emojis:
                if "ping" in emote.name.lower():
                    await message.add_reaction(emote)
                    break
        try:
            if message.content[0] in string.punctuation:
                try:
                    prefix = message.content[0]
                    cmd = message.content[1:].split(' ')[0]
                    for command in self.custom_commands[str(message.guild.id)]:
                        ncommand = self.custom_commands[str(message.guild.id)][command]
                        if cmd == ncommand['command'] and prefix == ncommand['prefix']:
                            response = ncommand['response']
                            response = response.replace('{author}', f'<@{message.author.id}>')
                            response = response.replace('{request}', f'{message.content[1+len(ncommand["command"]):]}')
                            await message.channel.send(content=response)
                            return
                        else:
                            continue
                    else:
                        pass
                except KeyError:
                    pass
        except IndexError:
            pass
        await self.process_commands(message)

    async def on_ready(self):
        await self.wait_until_ready()
        #   LOGGING
        logging_file = open('cogs/config/logging_channels.json', 'r')
        logging_data = json.loads(logging_file.read())
        logging_file.close()
        for guild in logging_data:
            self.logging_channels.setdefault(self.get_guild(int(guild)), self.get_channel(int(logging_data[guild])))
        #   WELCOME MESSAGE
        welcome_file = open('cogs/config/welcome_channels.json', 'r')
        welcome_data = json.loads(welcome_file.read())
        welcome_file.close()
        for guild in welcome_data:
                self.welcome_channels.setdefault(self.get_guild(int(guild)),
                                                 (self.get_channel(int(welcome_data[guild]["channel"])),
                                                  welcome_data[guild]["message"]))
        #   CUSTOM COMMAND RETRIEVER
        cc_file = open("cogs/config/custom_commands.json", 'r')
        cc_data = json.loads(cc_file.read())
        cc_file.close()
        self.custom_commands = cc_data
        #   SERVER DATA RETRIEVER
        for guild in self.guilds:
            if not str(guild.id) in self.server_data:
                try:
                    print(f"GENERATING DATA FOR {guild}")
                    dic = {
                        "prefix": "+"
                    }
                    self.server_data.setdefault(str(guild.id), dic)
                except TypeError:
                    continue
        #   MUTED ROLE GENERATOR
        for guild in self.guilds:
            try:
                for role in guild.roles:
                    if role.name == 'gamma_muted':
                        self.muted_roles.append(role)
    #                    print(f'FOUND MUTED ROLE FOR {guild.name}', self)
                        break
                else:
                    new = await guild.create_role(name='gamma_muted')
                    for channel in guild.channels:
                        ow = discord.PermissionOverwrite()
                        # noinspection PyDunderSlots,PyUnresolvedReferences
                        ow.send_messages = False
                        await channel.set_permissions(new, overwrite=ow)
                    self.muted_roles.append(new)
                    print(f'CREATED NEW ROLE FOR {guild.name}', self)
                    continue
            except discord.errors.Forbidden:
                continue
        #   FINALIZATION
        print('-'*20, self)
        print('Gamma-indev loaded.', self)
        print(f'Logged in as {self.user}', self)
        print(f'ID: {self.user.id}', self)
        print('-'*20, self)
        print(f"Muted roles:", self)
        for role in self.muted_roles:
            print("-"*20, self)
            print(f"Guild: {role.guild.name}", self)
            print(f"Name: {role.name}", self)
            print(f"ID: {role.id}", self)
        print('-'*20)
        print('Logging channels:')
        print('-'*20)
        for guild, channel in self.logging_channels.items():
            if guild is not None:
                print('#{1} ({0})'.format(guild, channel))
        print('-'*20)
        print('Welcome channels:')
        print('-'*20)
        for guild, channel in self.welcome_channels.items():
            try:
                print('#{1} says "{2}" ({0})'.format(guild, channel[0].name, channel[1]))
            except AttributeError:
                pass
        await self.change_presence(activity=discord.Game(name=f"{self.prefix}help",
                                                         type=discord.ActivityType.playing),
                                   status=discord.Status.online)

    async def on_error(self, event, *args, **kwargs):
        error = traceback.format_exc()
        to_send = f"An error occured in {event}:\n```{error}```"
        await self.get_channel(458771285414117387).send(to_send)
    
    async def on_command_error(self, ctx, e):
        if isinstance(e, commands.CommandNotFound):
            await ctx.message.add_reaction("❓")
            return
        if isinstance(e, commands.BadArgument):
            await ctx.message.add_reaction("❌")
            return
        await self.get_channel(458771285414117387).send(f"{type(e).__name__}: {e}")

    async def on_member_remove(self, member):
        embed = discord.Embed(title="User left the server.", description=f"<@{member.id}>", color=0xA16130)
        embed.set_author(name=f"{member}", icon_url=f"{member.avatar_url}")
        embed.set_thumbnail(url=f"{member.avatar_url}")
        embed.add_field(name="Time", value=f"{datetime.today().strftime('%A %d %B, %Y @ %I:%M%p')}", inline=False)
        try:
            await self.logging_channels[member.guild].send(embed=embed)
        except KeyError:
            pass
        return

    async def on_member_join(self, member):
        embed = discord.Embed(title="User joined the server.", description=f"<@{member.id}>", color=0x30a133)
        embed.set_author(name=f"{member}", icon_url=f"{member.avatar_url}")
        embed.set_thumbnail(url=f"{member.avatar_url}")
        embed.set_footer(text=f"{datetime.today().strftime('%A %d %B, %Y @ %I:%M%p')}")
        try:
            await self.logging_channels[member.guild].send(embed=embed)
            welcome = self.welcome_channels[member.guild][1].replace('@@',
                                                                     f'<@{member.id}>').replace('##',
                                                                                                f'{member.guild.name}')
            await self.welcome_channels[member.guild][0].send(content=welcome)
        except KeyError:
            pass
        return

    async def on_message_delete(self, message):
        try:
            purge = self.is_server_purging[message.guild]
        except KeyError:
            purge = False
        if purge or message.author.id == 453695925580333068:
            return
        embed = discord.Embed(title="Message was deleted.", description=f"<#{message.channel.id}>", color=0x9B2A2A)
        embed.set_author(name=f"{message.author}", icon_url=f"{message.author.avatar_url}")
        embed.add_field(name="Content", value=f"{message.content}" or "No content", inline=False)
        extras = "Embeds" if len(message.embeds) > 0 else None
        extras = f"{extras}, Attachments" if len(message.attachments) > 0 else extras
        if extras:
            embed.add_field(name="Extras", value=f"{extras}", inline=False)
        embed.set_footer(text=f"{datetime.today().strftime('%A %d %B, %Y @ %I:%M%p')}")
        try:
            await self.logging_channels[message.guild].send(embed=embed)
        except KeyError:
            pass
        return

    async def on_message_edit(self, before, after):
        if before.author.bot:
            return
        if before.content == after.content:
            return
        if len(before.embeds) > 0 or len(after.embeds) > 0:
            return
        embed = discord.Embed(title="Message was edited.", description=f"<#{after.channel.id}>", color=0x9B2A2A)
        embed.set_author(name=f"{after.author}", icon_url=f"{after.author.avatar_url}")
        embed.add_field(name="Before", value=f"{before.content}", inline=False)
        embed.add_field(name="After", value=f"{after.content}", inline=False)
        embed.set_footer(text=f"{datetime.today().strftime('%A %d %B, %Y @ %I:%M%p')}")
        try:
            await self.logging_channels[after.guild].send(embed=embed)
        except KeyError:
            pass
        return

    async def on_member_update(self, before, after):
        has_update = False
        if before.name != after.name:
            embed = discord.Embed(title="Users name was changed.", description=f"<@{after.id}>", color=0x9B2A2A)
            embed.set_author(name=f"{after}", icon_url=f"{after.avatar_url}")
            embed.add_field(name="Before", value=f"{before.name}", inline=False)
            embed.add_field(name="After", value=f"{after.name}", inline=False)
            embed.set_footer(text=f"{datetime.today().strftime('%A %d %B, %Y @ %I:%M%p')}")
            has_update = True
            try:
                await self.logging_channels[after.guild].send(embed=embed)
            except KeyError:
                pass
        if before.nick != after.nick:
            embed = discord.Embed(title="Users nickname was changed.", description=f"<@{after.id}>", color=0x9B2A2A)
            embed.set_author(name=f"{after}", icon_url=f"{after.avatar_url}")
            embed.add_field(name="Before", value=f"{before.nick}", inline=False)
            embed.add_field(name="After", value=f"{after.nick}", inline=False)
            embed.set_footer(text=f"{datetime.today().strftime('%A %d %B, %Y @ %I:%M%p')}")
            has_update = True
            try:
                await self.logging_channels[after.guild].send(embed=embed)
            except KeyError:
                pass
        if before.roles != after.roles:
            for role in after.roles:
                if role not in before.roles:
                    embed = discord.Embed(title="Users role was updated.", description=f"<@{after.id}>", color=0x9B2A2A)
                    embed.set_author(name=f"{after}", icon_url=f"{after.avatar_url}")
                    embed.add_field(name="Role given", value=f"<@&{role.id}>", inline=False)
                    embed.set_footer(text=f"{datetime.today().strftime('%A %d %B, %Y @ %I:%M%p')}")
                    has_update = True
                    try:
                        await self.logging_channels[after.guild].send(embed=embed)
                    except KeyError:
                        pass
            for role in before.roles:
                if role not in after.roles:
                    embed = discord.Embed(title="Users role was updated.", description=f"<@{after.id}>", color=0x9B2A2A)
                    embed.set_author(name=f"{after}", icon_url=f"{after.avatar_url}")
                    embed.add_field(name="Role taken", value=f"<@&{role.id}>", inline=False)
                    embed.set_footer(text=f"{datetime.today().strftime('%A %d %B, %Y @ %I:%M%p')}")
                    has_update = True
                    try:
                        await self.logging_channels[after.guild].send(embed=embed)
                    except KeyError:
                        pass
        if (before.status != after.status) or (before.activity != after.activity):
            has_update = True
        if not has_update:
            old = inspect.getmembers(before, lambda mem: not(inspect.isroutine(mem)))
            new = inspect.getmembers(after, lambda mem: not(inspect.isroutine(mem)))
            unmatched = []
            for a, b in zip(old, new):
                if a[1] != b[1]:
                    unmatched.append(b)
            if unmatched:
                if (unmatched[0][0] == 'avatar') or (unmatched[0][0] == 'avatar_url'):
                    embed = discord.Embed(title="Users avatar was updated.", description=f"<@{after.id}>",
                                          color=0x9B2A2A)
                    embed.set_author(name=f"{after}", icon_url=f"{after.avatar_url}")
                    embed.set_thumbnail(url=f"{before.avatar_url}")
                    embed.set_image(url=f"{after.avatar_url}")
                    embed.set_footer(text=f"{datetime.today().strftime('%A %d %B, %Y @ %I:%M%p')}")
                    try:
                        await self.logging_channels[after.guild].send(embed=embed)
                        return
                    except KeyError:
                        return
                await self.get_channel(458771285414117387).send(content=f"{unmatched}")
        return


if __name__ == "__main__":
    Gamma().run()
