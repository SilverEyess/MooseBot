import asyncio
import decimal

import discord
from discord.ext import commands
from discord.ext.commands import Cog

from moosebot import MooseBot


class Misc(Cog):

    def __init__(self, bot: MooseBot):
        self.bot = bot

    @commands.command()
    async def calc(self, ctx, *, args):
        dec = decimal.Context()
        dec.prec = 100

        def convert(f):
            d1 = dec.create_decimal(repr(f))
            return format(d1, 'f')

        args = args.split(',')
        args = ''.join(args)
        e = int(float(convert(eval(args))))
        await ctx.send(f'{e:,d}')

    @commands.command(help="Returns my gender.")
    async def gender(self, ctx):
        await ctx.send("I'm a boy, how could you not tell?")

    @Cog.listener()
    async def on_message(self, message):
        if message.author.id != 445936072288108544:
            await asyncio.gather(self.oreact(message), self.arrowreact(message))
        else:
            return

    async def arrowreact(self, message):
        arrows = [">", "<", "^", "v"]
        arrow = message.content
        if arrow.lower() in arrows:
            await message.channel.send(arrow)

    async def oreact(self, message):
        wordlist = ['o', '🇴', 'bet', 'k', "🇰"]
        OGs = [609238720532709386, 192519529417408512, 292493461268070411, 303280502960291840]
        if message.author.id in OGs:
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

