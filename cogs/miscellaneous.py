from discord.ext import commands
from datetime import datetime
from discord.utils import get
from discord.ext.commands.cooldowns import BucketType
from SimplePaginator import SimplePaginator
import discord
import numpy
import time
import random
import sys
import platform
import psutil

pyProcess = psutil.Process()


class Miscellaneous:
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def hello(self, ctx):
        await ctx.send("Hello "+ctx.message.author.mention)
    
    @commands.command(name="partyparrot")
    async def random_parrot(self, ctx, *, arg=None):
        parrots = [emote for emote in self.bot.emojis if "parrot" in emote.name.lower()]
        if arg is not None:
            await ctx.send(get(parrots, name=arg) or "No parrot " + arg + " found.")
        else:
            await ctx.send(random.choice(parrots))
            
    @commands.command(name="partyparrots")
    async def parrots(self, ctx):
        parrots = [str(emote)+" `"+emote.name+"`" for emote in self.bot.emojis if "parrot" in emote.name.lower()]
        parrots = list(set(parrots))
        await SimplePaginator(entries=parrots, colour=0xff0000, title="Party Parrots!", length=10).paginate(ctx)
    
    @commands.command(name="parrotwave")
    async def wave(self, ctx):
        parrotwaves = [emote for emote in self.bot.emojis if emote.name.lower().startswith("parrotwave")]
        await ctx.send(''.join(parrotwaves))
    
    @commands.command(name="congaparrot")
    async def conga(self, ctx, count: int, form=None):
        send = get(self.bot.emojis, name=f"{form or ''}congaparrot")
        send = str(send)*min(count, 50)
        if 'None' in send:
            await ctx.send("Invalid form.")
            return
        await ctx.send(send)
    
    @commands.command(aliases=["botinfo", "information"])
    async def info(self, ctx):
        embed = discord.Embed(title="A bot created by Xua#8831", description=f"ID: {self.bot.user.id}", color=0x65ace3)
        embed.set_author(name=f"{self.bot.user}", icon_url=f"{self.bot.user.avatar_url}")
        embed.set_thumbnail(url=f"{self.bot.user.avatar_url}")
        embed.add_field(name='Created', value=f'{self.bot.user.created_at.strftime("%a %d %b, %Y")}', inline=True)
        embed.add_field(name='Python Version', value=f'{sys.version[:5]}', inline=True)
        embed.add_field(name='discord.py Version', value=f'{discord.__version__}', inline=True)
        embed.add_field(name='CPU Usage', value=f'{pyProcess.cpu_percent()}%', inline=True)
        embed.add_field(name='Memory Usage', value=f'{round(pyProcess.memory_info()[0]/1024/1024,2)} MB', inline=True)
        embed.add_field(name='Website', value='[Click Here](https://xuathegrate.github.io/gamma/index.html)',
                        inline=True)
        embed.add_field(name='Latency', value=f'{round(self.bot.latency*1000,2)} ms', inline=True)
        embed.add_field(name='Server Prefix', value=f'{self.bot.get_pref(self.bot,ctx.message)}', inline=True)
        reboot = self.bot.reboot
        now = datetime.now()
        delta = (now - reboot).total_seconds()
        t = time.strftime("%H:%M:%S", time.gmtime(delta))
        last_reboot = f"{t[:2]}h, {t[3:5]}m, {t[6:8]}s"
        embed.add_field(name="Uptime", value=f"{last_reboot}", inline=True)
        embed.add_field(name="Source", value="[Click Here](https://github.com/XuaTheGrate/gammabot/)")
        embed.add_field(name="Host OS", value=f"{platform.platform()}", inline=True)
        embed.set_footer(text=f"Total Commands: {len(self.bot.commands)} | Total Cogs: {len(self.bot.cogs)} "
                              f"| Total Guilds: {len(self.bot.guilds)} | Total Members: {len(self.bot.users)}",
                         icon_url="https://cdn.discordapp.com/emojis/476643624679899147.png")
        await ctx.send(embed=embed)
    
    @commands.command()
    async def help(self, ctx):
        if not self.bot.debug:
            await ctx.send("View my commands here: <https://xuathegrate.github.io/gamma/index.html>")
        else:
            await ctx.send("View my commands here: <https://xuathegrate.github.io/gamma/index.html>\n"
                           ":warning: Sigma is the development build of Gamma. Be warned that many commands may"
                           " be missing/buggy.")
    
    @commands.cooldown(1, 5, BucketType.guild)
    @commands.command(usage="ping", brief="Check my connection time to discord.", description="~ping")
    async def ping(self, ctx):
        message = await ctx.send('Please wait...')
        creation = message.created_at
        await message.edit(content='Please wait... (Cycle 1)')
        firstedit = message.edited_at
        await message.edit(content='Please wait... (Cycle 2)')
        secondedit = message.edited_at
        await message.edit(content='Please wait... (Cycle 3)')
        thirdedit = message.edited_at
        ts1 = (firstedit - creation).microseconds
        ts2 = (secondedit - firstedit).microseconds
        ts3 = (thirdedit - secondedit).microseconds
        lst = [ts1, ts2, ts3]
        mean = numpy.mean(lst)
        mean = round(mean/1000, 2)
        await message.edit(content=f'PONG! `{mean}ms`')
    
    @ping.error
    async def ping_hander(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            seconds = error.retry_after
            seconds = round(seconds, 2)
            hours, remainder = divmod(int(seconds), 3600)
            minutes, seconds = divmod(remainder, 60)
            await ctx.send(f"You are on cooldown for another {minutes}m and {seconds}s.")

    @commands.command(name="whois", aliases=["user", "userinfo", "whodis"])
    async def whoami(self, ctx, user: discord.Member=None):
        user = user or ctx.author
        col = user.color if user.color.value > 0 else discord.Color(16777215)
        embed = discord.Embed(title="User information", description=f"<@{user.id}>", color=col)
        embed.set_author(name=f"{user}", icon_url=f"{user.avatar_url}")
        embed.set_thumbnail(url=f"{user.avatar_url}")
        reg_time = user.created_at.strftime("%a %d %b, %Y")
        embed.add_field(name='Registered', value=f'{reg_time}', inline=True)
        join_time = user.joined_at.strftime("%a %d %b, %Y")
        embed.add_field(name='Joined', value=f'{join_time}', inline=True)
        pos = sorted(user.guild.members, key=lambda m: m.joined_at).index(user)+1
        embed.add_field(name='Join Pos', value=f'{pos}', inline=True)
        embed.add_field(name='Status', value=f'{user.status}'.title(), inline=True)
        roles = [r.mention for r in user.roles if not r.is_default()]
        embed.add_field(name=f'Roles ({len(roles)})', value=f'{" ".join(roles)}', inline=False)
        embed.set_footer(text=f"ID: {user.id} | {datetime.today().strftime('%x')}")
        await ctx.send(embed=embed)
        return
        
    @commands.command(usage="source", brief="View my source code.", description="~source")
    async def source(self, ctx):
        await ctx.send("View my source code here: <https://github.com/XuaTheGrate/gammabot>")
        
    @commands.command(usage="uptime", brief="Check the uptime of the bot.", description="~uptime")
    async def uptime(self, ctx):
        reboot = self.bot.reboot
        now = datetime.now()
        delta = (now - reboot).total_seconds()
        t = time.strftime("%H:%M:%S", time.gmtime(delta))
        await ctx.send(f"Uptime: **{t[:2]}** hours, **{t[3:5]}** minutes, **{t[6:8]}** seconds"
                       f"\nLast reboot: {reboot.strftime('%A %d %B, %Y @ %H:%M')}")
        
    @commands.command(usage="bugreport", brief="Submit a bug report.", description="~bugreport")
    async def bugreport(self, ctx):
        await ctx.send("Found a bug in me? Oh boy time to for the doctors."
                       "\nReport the bug here: <https://goo.gl/forms/UDiwBURYbH16cPYj2>")
        
    @commands.command(usage="usercount", brief="Check the amount of users in the server.", description="~usercount")
    async def usercount(self, ctx):
        await ctx.send(f"There are `{len(ctx.message.guild.members)}` members in {ctx.message.guild.name}!")
    
    @staticmethod
    def manage_perm_or_xua(ctx):
        return ctx.message.author.permissions_in(ctx.message.channel).manage_messages or \
               ctx.message.author.id == 285915453094756362
    
    @commands.command()
    async def prefix(self, ctx, *pref):
        if len(pref) < 1:
            await ctx.send("This servers prefix is `"+self.bot.get_pref(self.bot, ctx.message)+'`')
            return
        if not self.manage_perm_or_xua(ctx) and pref is not None:
            await ctx.message.add_reaction("❌")
            return
        await ctx.send(await self.bot.update_prefix(ctx.message.guild, pref[0]))
        

def setup(bot):
    bot.remove_command("help")
    bot.add_cog(Miscellaneous(bot))
