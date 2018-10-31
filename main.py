from discord.ext import commands

from moosebot import MooseBot
from moosebot.cogs import *

with open('database/token.txt') as f:
    token = f.readline()

moose = MooseBot(token)
admins = ["192519529417408512", "345484068886020108"]


@moose.client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        print("{} is retarded and '{}' isn't a command.".format(ctx.author.display_name, ctx.message.content))


modules = [
    Misc(moose),
    Pet(moose),
    Shop(moose),
    Economy(moose),
    # TODO rewrite
    # Experience(moose),
    Info(moose),
    Counting(moose),
    Fun(moose),
    GuessGame(moose),
    Dad(moose),
    Moderation(moose),
    Server(moose),
    Voice(moose),
    Colour(moose),
    Numbers(moose),
    Phone(moose),
    Images(moose)
]

moose.add_cogs(modules)

moose.launch(token)