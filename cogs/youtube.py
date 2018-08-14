import aiohttp
import re
import urllib
from discord.ext import commands


class YouTube:
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def yt(self, ctx, *url):
        async with aiohttp.ClientSession() as session:
            alpha = "http://www.youtube.com/results?" + urllib.parse.urlencode({"search_query": url})
            # print(alpha)
            async with session.get(alpha) as response:
                beta = await response.text()
                # print(len(beta))
        urls = re.findall(r'href=\"/watch\?v=(.{11})', beta)
        first = f'http://www.youtube.com/watch?v={urls[0]}'
        await ctx.send(first)


def setup(bot):
    bot.add_cog(YouTube(bot))
