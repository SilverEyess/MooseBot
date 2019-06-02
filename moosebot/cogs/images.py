import discord
# from PIL import ImageFilter, Image
from discord.ext import commands

from moosebot import MooseBot
from moosebot.utils import *


class Images:

    def __init__(self, bot: MooseBot):
        self.bot = bot

    # @commands.command(
    #     help="Provide a user to sharpen their avatar or just an image to sharpen. Takes multiple passes to "
    #          "have visible effect.")
    # async def sharpen(self, ctx, *args):
    #     full_path = "database/avatar/temp_image.png"
    #     path = "database/avatar/"
    #     file_name = "temp_image"
    #     if len(ctx.message.mentions) == 1:
    #         user_avatar = ctx.message.mentions[0].avatar_url_as(format='png')
    #         data = get_image(user_avatar)
    #         save_image(path, file_name, data)
    #         im = Image.open(full_path)
    #         im_sharp = im.filter(ImageFilter.SHARPEN)
    #         im_sharp.save("database/avatar/temp_image.png", "PNG")
    #         await ctx.send(file=discord.File('database/avatar/temp_image.png'))
    #
    #     elif len(ctx.message.attachments) == 1:
    #         url = ctx.message.attachments[0].url
    #         data = get_image(url)
    #         save_image(path, file_name, data)
    #         im = Image.open(full_path)
    #         im_sharp = im.filter(ImageFilter.SHARPEN)
    #         im_sharp.save("database/avatar/temp_image.png", "PNG")
    #         await ctx.send(file=discord.File('database/avatar/temp_image.png'))
    #
    #     elif len(args) == 1 and args[0].startswith('http'):
    #         url = args[0]
    #         try:
    #             print(args[0])
    #             data = get_image(url)
    #             save_image(path, file_name, data)
    #             im = Image.open(full_path)
    #             im_sharp = im.filter(ImageFilter.SHARPEN)
    #             im_sharp.save("database/avatar/temp_image.png", "PNG")
    #             await ctx.send(file=discord.File('database/avatar/temp_image.png'))
    #         except Exception:
    #             await ctx.send("That url is invalid for whatever reason")
    #
    #     elif len(args) >= 1:
    #         memberlist = ctx.guild.members
    #         name = ' '.join(args)
    #         match = next(iter([x for x in iter(memberlist) if name.lower() == x.display_name.lower()]), None)
    #         if match is not None:
    #             match_index = memberlist.index(match)
    #             user_object = memberlist[match_index]
    #             user_url = user_object.avatar_url_as(format='png')
    #             data = get_image(user_url)
    #             save_image(path, file_name, data)
    #             im = Image.open(full_path)
    #             im_sharp = im.filter(ImageFilter.SHARPEN)
    #             im_sharp.save("database/avatar/temp_image.png", "PNG")
    #             await ctx.send(file=discord.File('database/avatar/temp_image.png'))
    #
    #     else:
    #         im = Image.open(full_path)
    #         im_sharp = im.filter(ImageFilter.SHARPEN)
    #         im_sharp.save("database/avatar/temp_image.png", "PNG")
    #         await ctx.send(file=discord.File('database/avatar/temp_image.png'))
