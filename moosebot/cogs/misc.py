import asyncio
import decimal
import json

import discord
from discord.ext import commands
from discord.ext.commands import Cog

from moosebot import MooseBot


class Misc(Cog):

    def __init__(self, bot: MooseBot):
        self.bot = bot

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

    # @Cog.listener()
    # async def on_member_update(self, before, after):
    #     if after.guild.id == 377218458108035084:
    #         if after.id == 488199047874740235:
    #             if after.display_name != before.display_name:
    #                 await after.edit(nick='The Best.')
    #                 print('Ana tried to change her nickname.')
    #             elif after.nick != before.nick:
    #                 await after.edit(nick='The Best.')
    #                 print('Ana tried to change her nickname.')
    #     else:
    #         return

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
