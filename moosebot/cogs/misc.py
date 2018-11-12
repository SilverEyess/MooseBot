import decimal

from discord.ext import commands

from moosebot import MooseBot


class Misc:

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
