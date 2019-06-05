import requests
from discord.ext import commands
from discord.ext.commands import Cog

from moosebot import MooseBot


class Numbers(Cog):

    def __init__(self, bot: MooseBot):
        self.bot = bot

    @commands.command(aliases=["sqr"], help="Squares a number. \n`>square number`")
    async def square(self, ctx, number):
        squared_value = float(number) * float(number)
        await ctx.send(str(number) + " squared is " + str(squared_value))

    @commands.command(aliases=["btc"], help="Returns the current price of bitcoin.")
    async def bitcoin(self, ctx):
        url = "https://api.coindesk.com/v1/bpi/currentprice/BTC.json"
        response = requests.get(url)
        value = response.json()["bpi"]["USD"]["rate"]
        await ctx.send("Bitcoin price is: $" + value)
