import discord
from discord.ext import commands
from discord.ext.commands import Cog

from moosebot import MooseBot, cog_group


@cog_group("Info")
class Server(Cog):

    def __init__(self, bot: MooseBot):
        self.bot = bot

    @commands.command(hidden=True)
    async def listsvr(self, ctx):
        embed = discord.Embed(title="Connected servers", description="List of servers that Moosebot is in.",
                              colour=0xb18dff)
        for i in self.bot.client.guilds:
            embed.add_field(name=i.name, value=f"**ID**: `{i.id}`", inline=False)
        await ctx.send(embed=embed)



def setup(bot):
    bot.add_cog(Server(bot.moose))
