from discord.ext import commands
from discord.ext.commands import CommandInvokeError

from moosebot import MooseBot
from moosebot.cogs import *

with open('database/token.txt') as f:
    token = f.readline().strip()

moose = MooseBot(token)
admins = ["192519529417408512", "536170543859105794"]

# @moose.client.event
# async def on_command_error(ctx, error):
#     if isinstance(error, commands.CommandNotFound):
#         print("{} is retarded and '{}' isn't a command.".format(ctx.author.display_name, ctx.message.content))
#     elif isinstance(error, CommandInvokeError):
#         await ctx.send(error.original)
#     else:
#         await ctx.send(f"some error lol {type(error.original)}")

extensions = [
    "moosebot.cogs.colour",
    "moosebot.cogs.counting",
    "moosebot.cogs.dad",
    "moosebot.cogs.economy",
    # TODO rewrite
    # "moosebot.cogs.experience",
    "moosebot.cogs.fishing",
    "moosebot.cogs.fun",
    "moosebot.cogs.guess_game",
    "moosebot.cogs.images",
    "moosebot.cogs.info",
    "moosebot.cogs.misc",
    "moosebot.cogs.moderation",
    "moosebot.cogs.numbers",
    "moosebot.cogs.pet",
    "moosebot.cogs.phone",
    "moosebot.cogs.server",
    "moosebot.cogs.shop",
    # "moosebot.cogs.voice",
]

for ext in extensions:
    moose.client.load_extension(ext)

moose.launch(token)
