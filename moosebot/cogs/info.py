import datetime

import discord
from discord.ext import commands
from discord.ext.commands import Cog

import geonamescache
import pytz
from moosebot import converters, MooseBot



class Info(Cog):

    def __init__(self, bot: MooseBot):
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
                      f"{member.activity}\n▫**Colour**: {str(member.colour).upper()}\n▫**Status**: {str(member.status).title()}"
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

    @commands.command(pass_context=True, help="Returns information about this bot.")
    async def info(self, ctx):
        embed = discord.Embed(title="MooseBot", description="This bot a moose.", colour=0xb18dff)
        embed.add_field(name="Author", value="<@192519529417408512>")
        embed.add_field(name='Contributors', value='<@488682312154742787>')
        embed.add_field(name="Server count", value=f"{len(self.bot.client.guilds)}")
        embed.add_field(name="Invite me to your server!",
                        value="[Invite link](https://discordapp.com/oauth2/authorize?client_id=445936072288108544&scope=bot&permissions=66186303)")
        embed.add_field(name="Join my server!", value="[Join here!](https://discord.gg/7Jcu6yn)")
        embed.add_field(name='Github', value='[Look at my trash code](https://github.com/SilverEyess/MooseBot)')
        embed.set_thumbnail(url=ctx.me.avatar_url)
        await ctx.send(embed=embed)

    @commands.command(help="Provides bot invite link.")
    async def invite(self, ctx):
        embed = discord.Embed(title="Moosebot invite", description="Invite Moosebot to your server!", colour=0xb18dff)
        embed.add_field(name="Invite",
                        value="Invite me using this **[link](https://discordapp.com/oauth2/authorize?client_id=445936072288108544&scope=bot&permissions=66186303)**")
        embed.set_thumbnail(url=ctx.me.avatar_url)
        await ctx.send(embed=embed)

    @commands.command(help="This is literally the help command.", aliases=['h'])
    async def help(self, ctx, *, arg: str = None):
        if arg is None:
            embed = discord.Embed(title="MooseBot", description="A bot that copies other bots and is also a Moose.",
                                  colour=0xb18dff)
            embed.add_field(name="Fun Commands",
                            value="`face` `guess` `8ball` `russian` `phone` `ping` `ship` `dadjoke` "
                                  "`embarrass` `greek` `letters` `thicc` `choose` `cointoss` `roll` "
                                  "`reverse` `rps` `urbandictionary` `translate` `square` `meme` "
                                  "`clap`",
                            inline=False)
            embed.add_field(name='Experience', value='`level` `leaderboard`', inline=False)
            embed.add_field(name='Economy', value='`pay` `steal` `coinflip` `balance` `balancelb`', inline=False)
            embed.add_field(name="Info Commands",
                            value="`server` `userinfo` `avatar` `bitcoin` `info` `invite` `emojis` "
                                  "`gender` `inrole` `feedback`", inline=False)
            embed.add_field(name="Admin commands", value="`kick` `ban` `clear` `count` `nickname` `moveto`",
                            inline=False)

            embed.set_thumbnail(url=ctx.me.avatar_url_as(format='png'))
            embed.set_footer(text=">help [command] to get help for that command.")
            await ctx.send(embed=embed)
        else:
            try:
                command = self.bot.client.get_command(name=arg)
                if command.help:
                    embed = discord.Embed(title=f"{command.name.title()} help.",
                                          description=f'{command.help} \n\n**Aliases**:\n{", ".join(command.aliases) if command.aliases else "None"}',
                                          colour=0xb18dff)
                    embed.set_thumbnail(url=ctx.me.avatar_url_as(format='png'))
                    await ctx.send(embed=embed)
                else:
                    await ctx.send("This command has no help text.")
            except AttributeError:
                await ctx.send(f"Command `{arg}` not found.")

    @commands.command(help="Get's a users avatar. \n`>avatar user`")
    async def avatar(self, ctx, *, member: converters.FullMember = None):
        member = member or ctx.author
        if member is not None:
            if isinstance(member, discord.Member):
                path = "database/avatar/"
                avatar = member.avatar_url
                await ctx.send(avatar)
                # data = get_image(avatar)
                # save_img(path, member.display_name, data)
            else:
                await ctx.send(f"Member `{member}` not found, try mentioning them to be certain.")
        else:
            await ctx.send(f"Member `{member}` not found, try mentioning them to be certain.")

    @commands.command(aliases=["ci"], help="Gives information about a city.")
    async def cityinfo(self, ctx, *, city=None):
        city = city.title() or None
        if city is None:
            await ctx.send("Tell me what city.")
        else:
            gc = geonamescache.GeonamesCache()
            cityinfo = gc.get_cities_by_name(city)
            try:
                if len(cityinfo) == 0:
                    await ctx.send("I can't find this city cus I'm dumb.")
                else:
                    for place in cityinfo:
                        for k in place:
                            cityinfo = place[k]
                            tz = pytz.timezone(cityinfo['timezone'])
                            tzinfo = datetime.datetime.now(tz)

                            description = f"**City Name:** {city.title()}\n **Country Code:**: {cityinfo['countrycode']}\n **Latitude & Longitude:** {cityinfo['latitude']}, {cityinfo['longitude']}" \
                                f"\n **Population:** ~{cityinfo['population']}\n **Date:** {tzinfo.strftime('%d-%b-%y')}\n **Time:** {tzinfo.strftime('%I:%M:%S %p')} "
                            embed = discord.Embed(title="City information.",description=description, colour=0xb18dff)
                            await ctx.send(embed=embed)
            except Exception:
                await ctx.send("I can't find this city cus I'm dumb.")
