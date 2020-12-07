import asyncio
import decimal
import json
import re

import discord
from discord.ext import commands
from discord.ext.commands import Cog

from moosebot import MooseBot


class Misc(Cog):

    def __init__(self, bot: MooseBot):
        from moosebot import MooseDb

        self.bot = bot
        self.database = MooseDb()
        self.db = self.database.db

    @commands.command()
    @commands.check(MooseBot.is_owner)
    async def eval(self, ctx, *, args):
        args = args.split(',')
        args = ''.join(args)
        e = eval(args)
        await ctx.send(e)

    @commands.command(help="Returns my gender.")
    async def gender(self, ctx):
        await ctx.send("I'm a boy, how could you not tell?")

    @Cog.listener()
    async def on_message(self, message):
        ctx = message.context
        await message.channel.send("test")
        user = ctx.bot.get_user(int(MooseBot.owner))
        serverid = str(message.guild.id)
        await user.message("Message got")
        server = await self.db.server.find_one({'serverid': serverid})

        if server is not None:
            await user.message("Message got")
            if 'reactblacklist' not in server:
                await user.message("reactblacklist not in server")
                await asyncio.gather(self.oreact(message), self.arrowreact(message), self.what(message.context))
            elif serverid in server['reactblacklist']:
                await user.message("serverid in list")
                return None
            elif str(message.channel.id) in server['reactblacklist']:
                await user.message("channelid in list")
                return None
            else:
                await user.message("else")
                await asyncio.gather(self.oreact(message), self.arrowreact(message), self.what(message.context))

        elif message.author.id != 192519529417408512:
            await asyncio.gather(self.oreact(message), self.arrowreact(message), self.what(message.context))

    async def arrowreact(self, message):
        arrows = [">", "<", "^", "v"]
        arrow = message.content
        if arrow.lower() in arrows:
            await message.channel.send(arrow)

    async def what(self, ctx):
        m = ctx.message.content.lower()

        whatlist = ["what", "wat", "wot", "wut", "scuseme"]
        for wat in whatlist:
            if m.strip(' ?!') == wat:
                message2 = await ctx.channel.history(before=ctx.message, limit=1).next()
                if message2.author == ctx.message.author:
                    await ctx.send("Are you dumb or something?")
                elif len(message2.embeds) >= 1:
                    await ctx.send("Yeah I'm not sure what they said either.")
                else:
                    unbolded = re.sub(r"\*\*(.+?)\*\*", r"\1", message2.content)
                    message = f"{message2.author.display_name} said: **{unbolded.upper()}**"
                    if len(message) > 2000:
                        await ctx.send("Yeah I'm not sure what they said either.")
                    else:
                        await ctx.send(message)

    async def oreact(self, message):
        wordlist = ['o', '🇴', 'bet', 'k', "🇰"]
        ogs = []
        for i in MooseBot.admins:
            ogs.append(i)
        ogs.append(MooseBot.owner)
        if str(message.author.id) in ogs:
            return
        elif message.content.lower() in wordlist:
            try:
                hook = await message.channel.create_webhook(name='ohook', avatar=None)
                await hook.send(
                    content=f"I don't actually know how to be a functioning human so I reply with '{message.content}' as a response",
                    username=message.author.display_name.ljust(2, '.'),
                    avatar_url=message.author.avatar_url)
                await hook.delete()
            except discord.Forbidden:
                await message.channel.send("I require the manage webhooks permission for this command to function.")


def setup(bot):
    bot.add_cog(Misc(bot.moose))
