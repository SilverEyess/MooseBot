import discord
from discord.ext import commands

from moosebot import MooseBot


class Colour:

    def __init__(self, bot: MooseBot):
        self.bot = bot

    @commands.command()
    async def colourme(self, ctx, arg):
        rolelist = ctx.author.roles
        name = ctx.author.display_name
        lowername = name.lower()
        colour = discord.Colour(int("0x" + arg, 16))
        for i in rolelist:
            print(i)
            if lowername == i.name.lower():
                await i.edit(colour=colour)
            else:
                await ctx.send("You do not possess a role with this ability")
