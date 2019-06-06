from discord.ext import commands
from discord.ext.commands import Cog

from moosebot import MooseBot


class Counting(Cog):

    def __init__(self, bot: MooseBot):
        self.bot = bot

    @commands.command()
    @commands.check(MooseBot.is_owner)
    async def count(self, ctx):
        if ctx.channel.topic and ctx.channel.topic.startswith(">count"):
            return None
        else:
            await ctx.channel.edit(topic=">count | The next message must start with 1")

    @Cog.listener()
    async def on_message(self, ctx):
        if ctx.guild is None:
            return None
        elif ctx.author == self.bot.client.user:
            return None
        else:
            if ctx.content.startswith(">count"):
                pass
            elif ctx.channel.topic and ctx.channel.topic.startswith(">count"):
                count = int(ctx.channel.topic.split()[8])
                if count is None:
                    return None
                elif ctx.content.startswith(f"{count} ") or ctx.content == str(count):
                    await ctx.channel.edit(topic=f">count | The next message must start with {count+ 1}")
                else:
                    await ctx.channel.purge(limit=1)
                    await ctx.channel.send(
                        f"{ctx.author.mention} The next message in this channel must start with {count}!",
                        delete_after=2.0)
