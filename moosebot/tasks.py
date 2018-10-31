import asyncio

import discord

from moosebot import MooseBot
from moosebot.utils import *


async def rad(bot: MooseBot, message):
    dard = bot.client.get_emoji(446703695204450305)
    if message.content == "<:rad:428937672552349698>":
        await message.add_reaction(dard)


async def dar(bot: MooseBot, message):
    radical = bot.client.get_emoji(428937672552349698)
    if message.content == "<:dar:446703695204450305>":
        await message.add_reaction(radical)


async def saveattach(bot: MooseBot, message):
    if message.author.id == bot.client.user.id:
        return None
    else:
        channel = message.guild.get_channel(449821022846320641)
        if channel is None:
            return
        if len(message.attachments) >= 1:
            path = "database/attachments/"
            for i in message.attachments:
                url = i.url
                data = get_image(url)
                file_name = str(i.id)
                file_type = i.url[-4:]
                types = [".png", ".mp4", ".jpg", ".gif", ".gifv", ".mp3", ".jpeg", ".mov"]
                if file_type in types:
                    save_image(path, file_name, data, file_type)
                else:
                    file_type = i.url[-5:]
                    if file_type in types:
                        save_image(path, file_name, data, file_type)
                    else:
                        file_type = ".png"
                        save_image(path, file_name, data, file_type)
                file_type = i.url[-4:]
                file_path = os.path.join(path, file_name + file_type)
                await asyncio.sleep(2)
                if message.guild.id == 427010987334434816:
                    await channel.send(file=discord.File(file_path))


async def mobile(bot: MooseBot, ctx):
    channel = ctx.channel
    if ctx.message.author.bot:
        return None
    elif ctx.message.content == ">phone":
        return None
    elif len(ctx.message.embeds) > 0:
        return None
    elif len(ctx.message.attachments) > 0:
        return None
    elif len(bot.phone_channels) == 2:
        if channel == bot.phone_channels[0]:
            await bot.phone_channels[1].send("**{}**#{}: {}".format(ctx.message.author.name,
                                                                    ctx.message.author.discriminator,
                                                                    ctx.message.content))
        elif channel == bot.phone_channels[1]:
            await bot.phone_channels[0].send("**{}**#{}: {}".format(ctx.message.author.name,
                                                                    ctx.message.author.discriminator,
                                                                    ctx.message.content))


async def what(ctx):
    m = ctx.message.content.lower()
    whatlist = ["what?", "wat?", "wot?", "scuseme?"]
    for wat in whatlist:
        if m == wat:
            message2 = await ctx.channel.history(before=ctx.message, limit=1).next()
            if len(message2.embeds) >= 1:
                await ctx.send("Yeah I'm not sure what they said either.")
            else:
                await ctx.send(f"{message2.author.display_name} said: **{message2.content.upper()}**")
