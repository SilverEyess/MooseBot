import asyncio

import discord
from discord.ext import commands
from discord.ext.commands import Cog

from moosebot import MooseBot, converters, cog_group


class Permissions(Cog):

    def __init__(self, bot: MooseBot):
        self.bot = bot
        self.db = self.bot.database.db

    @commands.command(aliases=["db"])
    @commands.check(MooseBot.is_admin)
    async def dadblacklist(self, ctx, arg=None):
        serverid = str(ctx.guild.id)
        channel = str(ctx.message.channel.id)
        server = await self.db.server.find_one({'serverid': serverid})

        if arg is None:
            await ctx.send("Please define whether to blacklist the guild or channel.")

        elif arg.lower() == "channel":
            if server is None:
                await self.db.server.update_one({'serverid': serverid}, {'$push': {'dadblacklist': channel}})
                await ctx.send("Channel added to dad blacklist.")
            elif 'dadblacklist' not in server:
                await self.db.server.update_one({'serverid': serverid}, {'$push': {'dadblacklist': channel}})
                await ctx.send("Channel added to dad blacklist.")
            elif channel in server['dadblacklist']:
                await self.db.server.update_one({'serverid': serverid}, {'$pull': {'dadblacklist': channel}})
                await ctx.send('Channel removed from dad blacklist.')
            else:
                await self.db.server.update_one({'serverid': serverid}, {'$push': {'dadblacklist': channel}})
                await ctx.send("Channel added to dad blacklist.")

        elif arg.lower() == "guild" or arg.lower() == "server":
            if server is None:
                await self.db.server.update_one({'serverid': serverid}, {'$push': {'dadblacklist': serverid}})
                await ctx.send("Guild added to dad blacklist.")
            elif 'dadblacklist' not in server:
                await self.db.server.update_one({'serverid': serverid}, {'$push': {'dadblacklist': serverid}})
                await ctx.send("Guild added to dad blacklist.")
            elif serverid in server['dadblacklist']:
                await self.db.server.update_one({'serverid': serverid}, {'$pull': {'dadblacklist': serverid}})
                await ctx.send("Guild removed from dad blacklist.")
            else:
                await self.db.server.update_one({'serverid': serverid}, {'$push': {'dadblacklist': serverid}})
                await ctx.send("Guild added to dad blacklist.")

        else:
            await ctx.send("Please define whether to blacklist the guild or channel.")


def setup(bot):
    bot.add_cog(Permissions(bot.moose))
