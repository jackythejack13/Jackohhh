import asyncio
import traceback
import psutil
import discord
import textwrap
import io
import sys
from discord.ext import commands
from contextlib import redirect_stdout

pyProcess = psutil.Process()


def resolve_user(u_resolvable, guild):
    if u_resolvable.startswith('<@'):
        u_resolvable = u_resolvable.strip('<@!>')
    try:
        u_resolvable = int(u_resolvable)
    except ValueError:
        pass
    if type(u_resolvable) == str:
        for member in guild.members:
            if u_resolvable.lower() in member.name.lower():
                return member
    if type(u_resolvable) == int:
        user = guild.get_member(u_resolvable)
        return user
    raise ValueError(f"No user {u_resolvable} found.")


class Debug:
    """Debugging commands."""
    def __init__(self, bot):
        self.bot = bot

    @commands.group(pass_context=True, hidden=True)
    @commands.is_owner()
    async def debug(self, ctx):
        pass

    @debug.command()
    async def say(self, ctx, *arg):
        async with ctx.message.channel.typing():
            to_send = ' '.join(arg)
            await asyncio.sleep(int(((len(to_send)/378)*60)))
            await ctx.send(f'{to_send}')

    @debug.command(name="exit")
    async def kill_me(self, ctx):
        await ctx.send("Logging out...")
        print("WARNING: Kill command was executed.")
        await self.bot.logout()
        sys.exit("Bot was exited via Debug")

    @debug.command(name="reload")
    async def _reload(self, ctx, cog):
        try:
            self.bot.unload_extension("cogs."+cog.lower())
            self.bot.load_extension("cogs."+cog.lower())
            await ctx.message.add_reaction("✅")
        except:
            error = traceback.format_exc()
            await ctx.message.add_reaction("❌")
            await ctx.send("```{}```".format(error))
    
    @debug.command()
    async def echo(self, ctx, channel, *msg):
        await self.bot.get_channel(int(channel)).send(' '.join(msg))
    
    @debug.command()
    async def cleanup(self, ctx, count: int=100):
        total = 0
        async for message in ctx.message.channel.history(limit=count):
            if message.author == self.bot.user:
                total += 1
                await message.delete()
        await ctx.send(f"Cleaned up **{total}** messages.", delete_after=2)
    
    @debug.command(name="save")
    async def save_server_data(self, ctx):
        await self.bot._save()
        await ctx.message.add_reaction("✅")

    @debug.command()
    async def user(self, ctx, user: resolve_user):
        await ctx.send(f"{user.mention}")

    @debug.command()
    async def muted_role(self, ctx):
        guild = ctx.message.guild
        role = await self.bot.get_muted_role(guild)
        await ctx.send(f'<@&{role.id}>')
            
    @debug.command()
    async def usage(self, ctx):
        to_send = f"""CPU Usage: {pyProcess.cpu_percent()}%
Memory Usage: {round(pyProcess.memory_info()[0]/1024/1024,2)}MB"""
        await ctx.send(to_send)
       
    @debug.command()
    async def logs(self, ctx):
        try:
            file = open('logs.txt', 'x')
        except FileExistsError:
            file = open('logs.txt', 'w')
        file.write(self.bot.logstring)
        file.close()
        with open('logs.txt', 'rb') as f:
            await ctx.send(file=discord.File(f, "logs.txt"))
            
    @debug.command()
    async def announce(self, ctx, *, arg):
        for guild in self.bot.guilds:
            try:
                await self.bot.logging_channels[guild].send(content=arg.replace("%%", f"<@{guild.owner.id}>"))
                await ctx.send(f'Successfully sent to {guild.name}.')
                continue
            except Exception:
                error = traceback.format_exc()
                await ctx.send(f'```py\n{error}```')
                continue


def setup(bot):
    bot.add_cog(Debug(bot))
