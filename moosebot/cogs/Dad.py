import random

from discord.ext import commands

from moosebot import MooseBot
from moosebot.utils import *


class Dad:

    def __init__(self, bot: MooseBot):
        self.blacklist = [442669193616162826]
        self.bot = bot

    @commands.command(aliases=["db"])
    @commands.check(MooseBot.is_owner)
    async def dadblacklist(self, ctx, arg=None):
        if arg is None:
            await ctx.send("Please define whether to blacklist the guild or channel.")
        elif arg.lower() == "channel":
            self.blacklist.append(ctx.channel.id)
            await ctx.send("Channel added to dad blacklist.")
        elif arg.lower() == "guild" or arg.lower() == "server":
            self.blacklist.append(ctx.guild.id)
            await ctx.send("Guild added to dad blacklist.")
        else:
            await ctx.send("Please define whether to blacklist the guild or channel.")

    async def on_message(self, message):
        ctx = await self.bot.client.get_context(message)
        if message.author == self.bot.client.user:
            return None
        elif isinstance(message.channel, discord.abc.PrivateChannel):
            return None
        elif message.channel.id in self.blacklist or message.guild.id in self.blacklist:
            return None
        else:
            await asyncio.gather(self.dad(message, ctx))

    async def dad(self, message, ctx):
        winner = random.choice([i for i in ctx.guild.members if not i.bot]).mention
        im_list = ("Retarded", "A sissy", "Boring <:sleeping:447382065474699265>",
                   "A NEET", "A drongo", "Regretting my life decisions that have brought me to this point",
                   "A very nice person", "A Weeb", "Abzy", "A heavy main", "A cunt", "A failure",
                   "Actually retarded", winner, f"{winner}'s partner in crime", f"{winner}'s secret admirer",
                   "About to get banned in a minute", "A thot", "A hoe", "A dumbass", "An ass", "Despacito", "Mexico",
                   "A fan of Muse")
        auth = message.author.id
        authname = ctx.author.display_name
        imlist = ["i'm", "im", "i am", "i m", "i’m"]
        lower = message.content.lower()

        for im in imlist:
            if lower.startswith(im + " dad") or lower.startswith(im + " father"):
                if auth == 192519529417408512:
                    try:
                        await ctx.me.edit(nick=authname + "'s child")
                        await ctx.send("Hi daddy <:heart_eyes:447658820529946624>")
                        await ctx.me.edit(nick=None)
                    except Exception:
                        await ctx.send("Hi daddy <:heart_eyes:447658820529946624>")
                else:
                    try:
                        await ctx.me.edit(nick=ctx.guild.name + "'s Dad")
                        await ctx.send(
                            "No {0.author.mention}, <@192519529417408512> is daddy <:heart_eyes:447658820529946624>.".format(
                                message))
                        await ctx.me.edit(nick=None)
                    except Exception:
                        await ctx.send("No {0.author.mention}, I'm dad.".format(message))
            elif lower == im:
                await ctx.send(random.choice(im_list))
            elif lower.startswith(im + " tler did nothing wrong"):
                await ctx.send("You're not funny {}".format(ctx.author.mention))
            elif lower.startswith(im + " mom") or lower.startswith(im + " mum"):
                if ctx.author.id == 495151300821123072:
                    await ctx.send("Hi mum.")
                else:
                    await ctx.send("No <@495151300821123072> is mum.")
            elif lower.startswith(im + " "):
                try:
                    users_dad = authname + "'s dad"
                    try:
                        await ctx.me.edit(nick=users_dad)
                        await ctx.send("Hi {}, I'm dad.".format(message.content[len(im) + 1:]))
                        await ctx.me.edit(nick=None)
                    except Exception:
                        await ctx.send("Hi {}, I'm dad.".format(message.content[len(im) + 1:]))
                finally:
                    try:
                        await ctx.me.edit(nick=None)
                    except Exception:
                        pass