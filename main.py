from discord.ext import commands
from discord.ext.commands import CommandInvokeError

from moosebot import MooseBot
import json
from moosebot.cogs import *

with open('database/config.json') as json_file:
    data = json.load(json_file)
    token = data['config'][0]['token']
    MooseBot.prefix = data['config'][0]['prefix']
    MooseBot.admins.append(data['config'][0]['owner'])
    MooseBot.owner = data['config'][0]['owner']
    admins = data['config'][0]['admins'].split(',')
    for i in admins:
        MooseBot.admins.append(i)
    print(MooseBot.admins)
    MooseBot.currency = data['config'][0]['currency']
    print(MooseBot.currency)
    print(MooseBot.owner)

# with open('database/token.txt') as f:
#     token = f.readline().strip()

moose = MooseBot(token)

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
    "moosebot.cogs.experience",
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
    "moosebot.cogs.permissions"
]

for ext in extensions:
    moose.client.load_extension(ext)

moose.launch(token)
