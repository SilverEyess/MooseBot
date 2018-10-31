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