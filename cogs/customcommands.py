from discord.ext import commands


class CustCommands:
    def __init__(self, bot):
        self.bot = bot
  
    @commands.group(pass_context=True, name="cc")
    @commands.has_permissions(manage_messages=True)
    @commands.bot_has_permissions(manage_messages=True)
    async def _custom_commands(self, ctx):
        pass
  
    @_custom_commands.command()
    async def create(self, ctx, prefix, command, *syntax):
        pass


def setup(bot):
    bot.add_cog(CustCommands(bot))
