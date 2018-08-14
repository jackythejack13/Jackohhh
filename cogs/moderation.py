import discord
import random
import asyncio
from discord.ext import commands
from datetime import datetime


def resolve_user(u_resolvable, guild):
    if u_resolvable.startswith('<@'):
        u_resolvable = u_resolvable.strip('<@!>')
    try:
        u_resolvable = int(u_resolvable)
    except ValueError:
        pass
    try:
        user = guild.get_member(u_resolvable)
        if not user:
            raise ValueError('E')
        return user
    except ValueError:
        user = guild.get_member_named(u_resolvable)
        if user is not None:
            return user
        raise ValueError(f"{u_resolvable} not found.")


"""
embed=discord.Embed(title="title", description="description", color=0x888888)
embed.set_author(name="author name")
embed.add_field(name="field 1 name", value="field 1 value", inline=False)
embed.add_field(name="field 2 name", value="field 2 value", inline=True)
embed.set_footer(text="footer text")
await self.bot.say(embed=embed)
"""


class Moderation:
    def __init__(self, bot):
        self.bot = bot
        self.cases = ['1']
        
    def next_moderation_case(self):
        alphanumeric = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I',
                        'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
        case = '1'
        while case in self.cases:
            case = '#'+''.join(["%s" % random.choice(alphanumeric) for num in range(15)])
        return case

    kick_usage = """~kick "Xua" "because why not"
~kick 285915453094756362 "because why not"
~kick @Xua "because why not" """

    @commands.command(aliases=["boot"], usage='kick <userID|userPing|"user name"> "<reason>"',
                      brief="Kick a user out of the server.", description=kick_usage)
    @commands.has_permissions(kick_members=True)
    @commands.bot_has_permissions(kick_members=True)
    async def kick(self, ctx, *kick):
        # !kick "Etherian Borealis" "being a gay fag"
        global kickee
        try:
            kickee = resolve_user(kick[0], ctx.message.guild)
        except IndexError:
            await ctx.message.add_reaction("❌")
            await ctx.send("Usage: ~kick <@user> [reason]")
        except ValueError:
            await ctx.message.add_reaction("❌")
            await ctx.send("User " + kick[0] + " was not found.")
        case = self.next_moderation_case()
        reason = ' '.join(kick[1:]) or "No reason specified."
        try:
            await ctx.message.guild.kick(kickee, reason=reason)
        except discord.errors.Forbidden:
            await ctx.message.add_reaction("❌")
            await ctx.send("I don't have permission to perform this command.")
            return
        try:
            await kickee.send(f"You were kicked from {ctx.message.guild.name}.\n"
                              f"Reason: {reason}\nModeration case {case}")
            dmed = True
        except Exception as e:
            dmed = False
            ctx.send(f"{type(e).__name__}: {e}")
            pass
        embed = discord.Embed(title="User kicked.",
                              description=f"{datetime.today().strftime('%A %d %B, %Y @ %I:%M%p')}",
                              color=0xA13030)
        embed.set_author(name=f"Moderation case {case}")
        embed.add_field(name="Moderator", value=f"<@{ctx.message.author.id}>", inline=False)
        embed.add_field(name="Kickee", value=f"<@{kickee.id}>", inline=True)
        embed.add_field(name="Reason", value=f"{reason}", inline=True)
        embed.set_footer(text=f"DMed user? {dmed}.")
        await self.bot.logging_channels[ctx.message.guild].send(embed=embed)
        await ctx.send(f"***{kickee} was kicked.***")

    @commands.command(usage='~ban <userID|userPing|"user name"> "<reason>"', brief="Swing the ban hammer on a user.",
                      description="""~ban "Xua" "lol fuck u"
~ban 285915453094756362 "lol fuck u"
~ban @Xua "lol fuck u" """)
    @commands.has_permissions(ban_members=True)
    @commands.bot_has_permissions(ban_members=True)
    async def ban(self, ctx, *ban):
        banee = resolve_user(ban[0], ctx.message.guild)
        case = self.next_moderation_case()
        reason = ' '.join(ban[1:]) or "No reason specified."
        try:
            await banee.send(f"You were banned from {ctx.message.guild.name}.\n"
                             f"Reason: {reason}\nModeration case {case}\n\n"
                             f"Contact a known moderator for info on how to appeal to this ban.")
            dmed = True
        except Exception:
            dmed = False
            pass
        embed = discord.Embed(title="User banned.",
                              description=f"{datetime.today().strftime('%A %d %B, %Y @ %I:%M%p')}",
                              color=0xA13030)
        embed.set_author(name=f"Moderation case {case}")
        embed.add_field(name="Moderator", value=f"<@{ctx.message.author.id}>", inline=False)
        embed.add_field(name="Banned user", value=f"<@{banee.id}>", inline=True)
        embed.add_field(name="Reason", value=f"{reason}", inline=True)
        embed.set_footer(text=f"DMed user? {dmed}.")
        await self.bot.logging_channels[ctx.message.guild].send(embed=embed)
        await ctx.message.guild.ban(banee, reason=reason, delete_message_days=7)
        await ctx.send(f"***{banee} was banned.***")

    @commands.command(usage="""~mute <userID|userPing|"user name"> "<reason>" """,
                      brief="Mute a user from typing in chat.",
                      description="""~mute "Xua" "rekt"
~mute 285915453094756362 "rekt"
~mute @Xua "rekt" """)
    @commands.has_permissions(manage_roles=True)
    @commands.bot_has_permissions(manage_roles=True)
    async def mute(self, ctx, *mute):
        """This command will mute a user, preventing them from typing in chat / adding reactions."""
        mutee = resolve_user(mute[0], ctx.message.guild)
        case = self.next_moderation_case()
        reason = ' '.join(mute[1:]) or "No reason specified."
        try:
            await mutee.send(f"You were muted in {ctx.message.guild.name}.\nReason: {reason}\nModeration case {case}.")
            dmed = True
        except Exception:
            dmed = False
            pass
        embed = discord.Embed(title="User muted.", description=f"{datetime.today().strftime('%A %d %B, %Y @ %I:%M%p')}",
                              color=0xA13030)
        embed.set_author(name=f"Moderation case {case}")
        embed.add_field(name="Moderator", value=f"<@{ctx.message.author.id}>", inline=False)
        embed.add_field(name="Muted user", value=f"<@{mutee.id}>", inline=True)
        embed.add_field(name="Reason", value=f"{reason}", inline=True)
        embed.set_footer(text=f"DMed user? {dmed}.")
        await self.bot.logging_channels[ctx.message.guild].send(embed=embed)
        await mutee.add_roles(await self.bot.get_muted_role(ctx.message.guild), reason=reason)
        await ctx.send(f"***{mutee} was muted.***")

    @commands.command(usage="""~unmute <userID|userPing|"user name">""", brief="Unmute a user.",
                      description="""~unmute "Xua"\n~unmute 285915453094756362\n~unmute @Xua""")
    @commands.has_permissions(manage_roles=True)
    @commands.bot_has_permissions(manage_roles=True)
    async def unmute(self, ctx, *mute):
        """This command will unmute a user, allowing them to type in chat again."""
        mutee = resolve_user(mute[0], ctx.message.guild)
        await mutee.remove_roles(await self.bot.get_muted_role(ctx.message.guild))
        case = self.next_moderation_case()
        embed=discord.Embed(title="User unmuted.", description=f"{datetime.today().strftime('%A %d %B, %Y @ %I:%M%p')}",
                            color=0xA13030)
        embed.set_author(name=f"Moderation case {case}")
        embed.add_field(name="Moderator", value=f"<@{ctx.message.author.id}>", inline=False)
        embed.add_field(name="Unmuted user", value=f"<@{mutee.id}>", inline=True)
        await self.bot.logging_channels[ctx.message.guild].send(embed=embed)
        await ctx.send(f"***{mutee} was unmuted.***")

    @commands.command(aliases=["quickban"], usage="""~softban <userID|userPing|"user name"> "<reason>" """, 
                      brief="Kick a user and delete their messages.", description="""~softban "Xua" "lul"
~softban 285915453094756362 "lul"
~softban @Xua "lul" """)
    @commands.has_permissions(kick_members=True)
    @commands.bot_has_permissions(ban_members=True)
    async def softban(self, ctx, *kick):
        """Bans and instantly unbans a user to delete their messages."""
        kickee = resolve_user(kick[0], ctx.message.guild)
        case = self.next_moderation_case()
        reason = ' '.join(kick[1:]) or "No reason specified."
        try:
            await kickee.send(f"You were kicked from {ctx.message.guild.name}.\n"
                              f"Reason: {reason}\nModeration case {case}.")
            dmed = True
        except Exception:
            dmed = False
            pass
        embed = discord.Embed(title="User soft-banned.",
                              description=f"{datetime.today().strftime('%A %d %B, %Y @ %I:%M%p')}", color=0xA13030)
        embed.set_author(name=f"Moderation case {case}")
        embed.add_field(name="Moderator", value=f"<@{ctx.message.author.id}>", inline=False)
        embed.add_field(name="Kicked user", value=f"<@{kickee.id}>", inline=True)
        embed.add_field(name="Reason", value=f"{reason}", inline=True)
        embed.set_footer(text=f"DMed user? {dmed}.")
        await self.bot.logging_channels[ctx.message.guild].send(embed=embed)
        await ctx.message.guild.ban(kickee, reason=reason, delete_message_days=7)
        await ctx.message.guild.unban(kickee)
        await ctx.send(f"***{kickee} was kicked.***", )
        
    @commands.command(aliases=["prune"], usage='purge <numMessages>', brief="Purge a number of messages.",
                      description='~purge 50')
    @commands.has_permissions(manage_messages=True)
    @commands.bot_has_permissions(manage_messages=True)
    async def purge(self, ctx, *purge):
        """Deletes a number of messages from a channel."""
        self.bot.is_server_purging[ctx.message.guild] = True
        overall = int(purge[0])+1
        if overall <= 0:
            await ctx.send("You must purge at least 1 message!")
            return
        times = int(overall / 100)
        extra = overall % 100
        success = 0
        fail = 0
        purged_messages = []
        for a in range(times):
            try:
                purged_messages.extend(await ctx.message.channel.purge(limit=100))
                success += 100
            except Exception as error:
                formaterror = "{}: {}".format(type(error).__name__, error)
                await ctx.send(f"An error occured deleting the messages.\n{formaterror}")
                fail += 100
        if extra > 0:
            try:
                purged_messages.extend(await ctx.message.channel.purge(limit=extra))
                success += extra
            except Exception as error:
                formaterror = "{}: {}".format(type(error).__name__, error)
                await ctx.send(f"An error occured deleting the messages.\n{formaterror}")
                fail += extra
        case = self.next_moderation_case()
        embed = discord.Embed(title="Chat purged.",
                              description=f"{datetime.today().strftime('%A %d %B, %Y @ %I:%M%p')}",
                              color=0xA13030)
        embed.set_author(name=f"Moderation case {case}")
        embed.add_field(name="Moderator", value=f"<@{ctx.message.author.id}>", inline=False)
        embed.add_field(name="Total messages deleted", value=f"{success}", inline=True)
        await self.bot.logging_channels[ctx.message.guild].send(embed=embed)
        await ctx.send(f"***Purged {success-1} messages. ({fail} deletions failed.)***", delete_after=2)
        await asyncio.sleep(1)
        purge_data = open(f"purgelogs/{case.replace('#','')}.txt", "x")
        for message in purged_messages:
            purge_data.write(f"[{message.created_at}] {message.author}: {message.content}\n")
        purge_data.close()
        self.bot.is_server_purging[ctx.message.guild] = False
        
    @commands.command(name="purge_logs")
    @commands.has_permissions(manage_messages=True)
    @commands.bot_has_permissions(attach_files=True)
    async def logs(self, ctx, purge_id):
        try:
            with open(f"purgelogs/{purge_id}.txt", "rb") as f:
                await ctx.send(f"<@{ctx.message.author.id}>, here are the logs for purge id {purge_id}",
                               file=discord.File(f, f"purge_{purge_id}.txt"))
                return
        except FileNotFoundError:
            await ctx.send(f"No purge logs of that ID were found.\n`Note: The logs get cleared every 24 hours.`")
            return
                

def setup(bot):
    bot.add_cog(Moderation(bot))
