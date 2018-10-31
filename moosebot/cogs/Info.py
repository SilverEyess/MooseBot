import datetime

import discord
from discord.ext import commands

from moosebot import converters


class Info:

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def roles(self, ctx, user: converters.FullMember = None):
        user = user or ctx.author
        roles = '\n'.join([x.name for x in user.roles][1:])
        embed = discord.Embed(title=f"{user.display_name}'s roles.", description=roles, colour=0xb18dff)
        embed.set_thumbnail(url=user.avatar_url)

        await ctx.send(embed=embed)

    @commands.command(aliases=["fb"], help="Send feedback to the bot author. \n`>feedback what you want to send here`")
    async def feedback(self, ctx, *, arg):
        user = ctx.bot.get_user(192519529417408512)
        embed = discord.Embed(
            title=f"Feedback from {ctx.author.name}({ctx.author.id}) on {ctx.guild.name}({ctx.guild.id}):",
            description=arg, colour=0xb18dff)
        await user.send(embed=embed)
        await ctx.send("Feedback sent! Thank you!")

    @commands.command(help="Give a role name to get a list of users in that role. \n`>inrole rolename`")
    async def inrole(self, ctx, *, role: converters.Role):
        users = [x.display_name for x in role.members]
        embed = discord.Embed(
            title=f"{len(role.members)} {'users' if len(role.members) != 1 else 'user'} in {role.name}",
            description=f"`{'`, `'.join(users)}`",
            colour=0xb18dff if role.colour == discord.Colour(000000) else role.colour)
        await ctx.send(embed=embed)

    @inrole.error
    async def inrole_error(self, ctx, error):
        await ctx.send(error)

    @commands.command(aliases=['user', 'ui'], help="Provides information about a user. \n`>ui user`")
    async def userinfo(self, ctx, *, member: converters.FullMember = None):
        member = member or ctx.author
        member_date = datetime.date(member.created_at.year, member.created_at.month, member.created_at.day)
        age = datetime.date.today() - member_date
        roles = [f"`{i.name}`" for i in member.roles]
        if member == ctx.guild.owner:
            isowner = "👑__**Guild owner**__👑\n"
        else:
            isowner = ""
        description = f"{isowner}▫**User ID**: `{member.id}`\n▫**Join Date**: {member.joined_at.strftime('%d/%m/%Y')}\n" \
                      f"▫**Account Created**: {member.created_at.strftime('%d/%m/%Y')}\n▫**Account Age**: {age.days} days" \
                      f"\n▫**Voice Channel**: {member.voice.channel.name if member.voice else 'None'}\n▫**Playing Now**: " \
                      f"{member.game}\n▫**Colour**: {str(member.colour).upper()}\n▫**Status**: {str(member.status).title()}"
        embed = discord.Embed(title=f"User info for {member}", description=description,
                              colour=0xb18dff if member.colour == discord.Colour(000000) else member.colour)
        if len(member.roles) > 1:
            embed.add_field(name=f"Roles: [{len(member.roles) - 1}]", value=', '.join(roles[1:]))
        else:
            embed.add_field(name=f"Roles: [{len(member.roles) - 1}]", value="No custom roles.")
        embed.set_thumbnail(url=member.avatar_url)
        await ctx.send(embed=embed)

    @userinfo.error
    async def userinfo_error(self, ctx, error):
        await ctx.send(error)
