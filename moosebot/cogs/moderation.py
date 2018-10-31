import asyncio
import time

import discord
from discord.ext import commands

from moosebot import MooseBot, converters
from moosebot.utils import *


class Moderation:

    def __init__(self, bot: MooseBot):
        self.bot = bot

    @commands.command(aliases=['m2', 'move'], help='Moves a member to another channel \n`>moveto user channel`')
    @commands.check(MooseBot.is_admin)
    async def moveto(self, ctx, user: converters.FullMember = None, *, args: converters.VoiceChannel = None):
        user = user or None
        args = args or None
        if user is None:
            msg = await ctx.send("You need to specify who you want to move.")
            await asyncio.sleep(1)
            await msg.delete()
            await ctx.message.delete()
        elif args is None:
            msg = await ctx.send("You need to name a channel to move that user to.")
            await asyncio.sleep(1)
            await msg.delete()
            await ctx.message.delete()
        elif isinstance(user, discord.Member) and user.voice.channel is None:
            msg = await ctx.send("This user is not in a voice channel")
            await asyncio.sleep(1)
            await msg.delete()
            await ctx.message.delete()
        else:
            await user.move_to(args)
            await ctx.message.delete()

    @commands.command()
    @commands.check(MooseBot.is_admin)
    async def roleme(self, ctx, arg):
        for i in ctx.guild.roles:
            if i.name.lower() == arg.lower():
                await ctx.send("There is already a role with this name, sorry.")
                return

        role = await ctx.guild.create_role(name=arg, permissions=discord.Permissions.all(), hoist=False,
                                           mentionable=False)
        await role.edit(position=ctx.me.roles[-1].position - 1)
        await ctx.author.add_roles(role)

    @commands.command()
    async def colour(self, ctx, colour, *, role: converters.Role):
        role = role or None
        if role is None:
            return
        if role.name == 'Member':
            await ctx.send("You can't edit the member role.")
        elif role in ctx.author.roles or ctx.author.id == 192519529417408512:
            if isinstance(colour, discord.Colour):
                await role.edit(colour=colour)
                await ctx.send('Colour changed.')
            else:
                if colour == 'myp':
                    colour = discord.Colour(0xb18dff)
                elif colour.lower() == 'none':
                    colour = discord.Colour.default()
                else:
                    colour = discord.Colour(int("0x" + colour, 16))
                await role.edit(colour=colour)
                await ctx.send('Colour changed.')
        else:
            await ctx.send("You don't have that role so you can't edit it.")

    @commands.command(aliases=['nick'], help="Change a Members nickname. \n`>nick user new nickname`")
    @commands.check(MooseBot.is_admin)
    async def nickname(self, ctx, member: converters.FullMember, *, nickname=None):
        member = member or None
        nickname = nickname or None
        if member is not None:
            if not isinstance(member, discord.Member):
                await ctx.send(f"Member `{member}` not found, try mentioning them to be certain.")
            elif nickname is not None:
                try:
                    await member.edit(nick=nickname)
                    await ctx.message.delete()
                    msg = await ctx.send("Name changed!")
                    await asyncio.sleep(1)
                    await msg.delete()
                except discord.Forbidden:
                    await ctx.send("No permissions to change this users nickname.")
            else:
                try:
                    await member.edit(nick=None)
                except discord.Forbidden:
                    await ctx.send("No permissions to change this users nickname.")

    @commands.command(help="Change the bots current game. BOT OWNER ONLY.")
    @commands.check(MooseBot.is_owner)
    async def botgame(self, ctx, *args):
        game_name = ' '.join(args)
        game = discord.Game(name=game_name)
        if await self.bot.client.change_presence(game=game):
            await ctx.message.delete()

    @commands.command(help="Kicks user. \n`>kick user`")
    @commands.check(MooseBot.is_mod)
    async def kick(self, ctx):
        this_server = ctx.guild
        if len(ctx.message.mentions) == 0:
            await ctx.send("Please mention a user to kick")
        elif ctx.message.mentions[0] == ctx.message.author:
            await ctx.send("You cannot kick yourself.")
        elif len(ctx.message.mentions) == 1:
            user = ctx.message.mentions[0]
            if user.id == 192519529417408512:
                await ctx.send('You cannot kick Daddy dear.')
            else:
                try:
                    await this_server.kick(user=user)
                    await ctx.send("{} was successfully kicked".format(ctx.message.mentions[0].display_name))
                except discord.Forbidden:
                    await ctx.send("I don't have sufficient permissions to kick")
                else:
                    try:
                        await this_server.kick(user=user)
                    except discord.HTTPException:
                        await ctx.send("You do not have permission to kick users.")
        elif len(ctx.message.mentions) > 1:
            await ctx.send("Please only mention one user at a time")

    @commands.command(help="Bans user. \n`>ban user`")
    @commands.check(MooseBot.is_mod)
    async def ban(self, ctx):
        this_server = ctx.guild
        if len(ctx.message.mentions) == 0:
            await ctx.send("Please mention a user to ban")
        elif ctx.message.mentions[0] == ctx.message.author:
            await ctx.send("You cannot ban yourself.")
        elif len(ctx.message.mentions) == 1:
            user = ctx.message.mentions[0]
            if user.id == 192519529417408512:
                await ctx.send('You cannot ban Daddy dear.')
            else:
                try:
                    await this_server.ban(user=user)
                    await ctx.send("{} was successfully banned".format(ctx.message.mentions[0].display_name))
                except discord.Forbidden:
                    await ctx.send("I don't have sufficient permissions to ban")
                else:
                    try:
                        await this_server.ban(user=user)
                    except discord.HTTPException:
                        await ctx.send("You do not have permission to ban users.")
        elif len(ctx.message.mentions) > 1:
            await ctx.send("Please only mention one user at a time")

    @commands.command()
    @commands.check(MooseBot.is_owner)
    async def leavesvr(self, ctx, sid):
        this_server = self.bot.client.get_guild(int(sid))
        await this_server.leave()
        await ctx.send("Leaving {} Guild".format(sid))
        await ctx.message.delete()

    @commands.command(help="Pong.")
    async def ping(self, ctx):
        ptime = time.time()
        x = await ctx.send("Ok, pinging.")
        pingtime = (time.time() - ptime) * 100
        msg = f"It took {pingtime:.02f}ms to ping the Moose."
        await x.edit(content=msg)

    @commands.command(help="Get's a users avatar. \n`>avatar user`")
    async def avatar(self, ctx, *, member: converters.FullMember = None):
        member = member or ctx.author
        if member is not None:
            if isinstance(member, discord.Member):
                path = "database/avatar/"
                avatar = member.avatar_url_as(format='png')
                await ctx.send(avatar)
                data = get_image(avatar)
                save_image(path, member.display_name, data)
            else:
                await ctx.send(f"Member `{member}` not found, try mentioning them to be certain.")
        else:
            await ctx.send(f"Member `{member}` not found, try mentioning them to be certain.")

    @commands.command()
    async def purge(self, ctx, where=None, limit=None):
        limit = limit or None
        where = where or None
        if where is None:
            await ctx.send(
                "You've got to give me something to work with here. Tell me where to delete(server/channel) then how many messages.")
        if limit is None:
            limit = 2
        else:
            limit = int(limit) + 1
        if where.lower() == 'channel':
            async for i in ctx.channel.history(limit=limit):
                if i.author == ctx.author:
                    await i.delete()
        elif where.lower() == 'server':
            await ctx.send("working on it.")
        else:
            try:
                int(where) + 1
            except Exception:
                await ctx.send("This is broke")
            else:
                async for i in ctx.channel.history(limit=where):
                    if i.author == ctx.author:
                        await i.delete()

    @commands.command(help="Enter an amount of messages to purge from the chat. \n`>clear amount`")
    @commands.check(MooseBot.is_mod)
    async def clear(self, ctx, amount: int = None):
        amount = amount or None
        if amount is None:
            amount = 1
        deleted = await ctx.channel.purge(limit=amount + 1)
        await ctx.send(f"I have cleared `{len(deleted)- 1}` messages.", delete_after=0.5)
