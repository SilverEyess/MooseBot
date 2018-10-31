import asyncio
import random

import discord
from discord.ext import commands

from moosebot import MooseBot, converters


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
            await self.dad(message, ctx)

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

    def dadload(self, path):
        dadjokes = []
        with open(path, "r") as f:
            for entry in f.readlines():
                dadjokes.append(entry.rstrip())
        return dadjokes

    def dadsave(self, path, dadjokes):
        with open(path, "w") as f:
            for entry in dadjokes:
                f.write(entry + "\n")

    @commands.command(
        help="Returns a quality dadjoke. Or try to add/remove jokes(If bot author on your server) \n`>dadjoke add/remove joke`")
    async def dadjoke(self, ctx, *args):
        path = "database/dadjokes.txt "
        dadjokes = self.dadload(path)
        emoji = " <:lmoa:446850171134017536>"
        bottle = self.bot.client.get_user(192519529417408512)

        if not args:
            dadjokes.append(emoji)
            await ctx.send(random.choice(dadjokes).replace("|", "\n") + emoji)
        elif args[0].lower() == "add":
            joke = ' '.join(args[1:])
            await ctx.send("{} Add this joke to dadjokes? <Yes/No> \n \n '{}'".format(bottle.mention, joke))

            def check(m):
                return m.content.lower() == "yes" or m.content.lower() == "no"

            msg = await self.bot.client.wait_for('message', check=check)

            if msg.content == 'yes' or msg.content == 'Yes' and msg.author == bottle:
                await ctx.send("{} Your joke was added to the list of dadjokes!".format(ctx.author.mention))
                dadjokes.append(joke)
                self.dadsave(path, dadjokes)

            elif msg.content == 'no' or msg.content == 'No' and msg.author == bottle:
                await ctx.send("Your joke was not added, make sure it's formatting is correct"
                               " with a | at the beginning of a new line, otherwise it was just a bad joke, "
                               "not a dad joke.")
        elif args[0].lower() == "del" or args[0].lower() == "delete":
            joke = ' '.join(args[1:])
            await ctx.send("{} Delete this joke from dadjokes? <Yes/No> \n \n '{}'".format(bottle.mention, joke))

            def check(m):
                return m.content == "yes" or m.content == "no"

            msg = await self.bot.client.wait_for('message', check=check)

            if msg.content.lower() == 'yes':
                match = next(iter([x for x in iter(dadjokes) if x.lower() == joke.lower()]), None)
                if match is not None:
                    dadjokes.remove(match)
                    await ctx.send("'{}'\n The above joke was deleted from dadjokes".format(joke))
                    self.dadsave(path, dadjokes)
                else:
                    await ctx.send("That joke is not in the list")
        elif args[0].lower() == "list":
            await ctx.send(dadjokes)
        else:
            await ctx.send("That's not an option for this command")

    @commands.command(aliases=["emb"], help="Embarrasses you or a friend! \n`>embarrass` \n`>embarrass user`")
    async def embarrass(self, ctx, arg: converters.PartialMember = None, *, args=None):
        path = "database/embarrass.txt"
        embarrass_list = Dad.load_embarrass(path)
        bottle = self.bot.client.get_user(192519529417408512)
        arg = arg or None
        args = args or None
        if arg is None:
            try:
                hook = await ctx.channel.create_webhook(name="Dadhook", avatar=None)
                await hook.send(content=random.choice(embarrass_list), username=ctx.author.display_name.ljust(2, '.'),
                                avatar_url=ctx.author.avatar_url)
                await hook.delete()
            except discord.Forbidden:
                await ctx.send("I require the manage webhooks permission for this command to function.")
        elif isinstance(arg, discord.Member):
            try:
                hook = await ctx.channel.create_webhook(name="Dadhook", avatar=None)
                await hook.send(content=random.choice(embarrass_list), username=arg.display_name.ljust(2, ','),
                                avatar_url=arg.avatar_url)
                await hook.delete()
            except discord.Forbidden:
                await ctx.send("I require the manage webhooks permission for this command to function.")
        elif arg.lower() == "add" or arg.lower() == "a":
            if args is None:
                await ctx.send("You need to enter a phrase to suggest being added to the embarrass list.")
            else:

                await ctx.send(f"{bottle.mention} add this phrase to the embarrass list? Y/N \n\n `{args}`")

                def check(m):
                    return m.content.lower() == "yes" or m.content.lower() == "y" or m.content.lower() == "no" or m.content.lower() == "n" and m.author.id == 192519529417408512

                try:
                    msg = await self.bot.client.wait_for('message', check=check, timeout=10)
                    if msg.content.lower() == 'yes' or msg.content.lower() == 'y':
                        await ctx.send("Adding phrase to embarrass list.")
                        embarrass_list.append(args)
                        Dad.save_embarrass(path, embarrass_list)
                    elif msg.content.lower() == 'no' or msg.content.lower() == 'n':
                        await ctx.send(f"Your phrase has been denied {ctx.author.mention}")

                except asyncio.TimeoutError:
                    await ctx.send("Daddy didn't respond in time, try again later.")
        elif arg.lower() == "del" or arg.lower() == "delete" or arg.lower() == "d":
            if args is None:
                await ctx.send("You need to enter a phrase to suggest being deleted from the embarrass list.")
            else:
                match = next(iter([x for x in iter(embarrass_list) if x.lower() == args.lower()]), None)
                if match is None:
                    await ctx.send("That phrase was not found in the embarrass list.")
                else:
                    await ctx.send(f"{bottle.mention} remove this phrase from the embarrass list? Y/N \n\n `{args}`")

                    def check(m):
                        return m.content.lower() == "yes" or m.content.lower() == "y" or m.content.lower() == "no" or m.content.lower() == "n" and m.author.id == 192519529417408512

                    try:
                        msg = await self.bot.client.wait_for('message', check=check, timeout=10)
                        if msg.content.lower() == 'y' or msg.content.lower() == 'yes':
                            await ctx.send("Removing the phrase from the embarras list.")
                            embarrass_list.remove(match)
                            Dad.save_embarrass(path, embarrass_list)
                        elif msg.content.lower() == 'n' or msg.content.lower() == 'no':
                            await ctx.send("Your suggestion to remove that phrase has been denied {ctx.author.mention}")

                    except asyncio.TimeoutError:
                        await ctx.send("Daddy didn't respond in time, try again later.")
        elif arg.lower() == 'l' or arg.lower() == 'list':
            embed = discord.Embed(title="Embarrassing phrases", description='\n'.join(embarrass_list))
            await ctx.send(embed=embed)
        else:
            await ctx.send("That's not an option for this command")

    @staticmethod
    def load_embarrass(path):
        embarrass_list = []
        with open(path, "r") as f:
            for entry in f.readlines():
                embarrass_list.append(entry.rstrip())
        return embarrass_list

    @staticmethod
    def save_embarrass(path, embarrass_list):
        with open(path, "w") as f:
            for entry in embarrass_list:
                f.write(entry + "\n")