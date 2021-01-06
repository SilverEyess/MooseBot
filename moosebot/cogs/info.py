import datetime
from collections import OrderedDict
import json
import requests

import discord
from discord.ext import commands
from discord.ext.commands import Cog

import geonamescache
import pytz
from moosebot import converters, MooseBot


class Info(Cog):
    from moosebot.cogs import Voice, Experience, Pet
    ignored_cogs = [Voice, Experience, Pet]

    def __init__(self, bot: MooseBot):
        self.bot = bot

    @commands.command(help="Returns all emojis on this server")
    async def emojis(self, ctx):
        emojisl = []
        for i in ctx.guild.emojis:
            if i.animated:
                emojisl.append(f"<a:{i.name}:{i.id}> `:{i.name}:` \n")
            else:
                emojisl.append(f"<:{i.name}:{i.id}> `:{i.name}:` \n")
        emoji_list = ''.join(emojisl)
        await ctx.send(emoji_list)

    @commands.command(help="Returns information about this guild.", aliases=["guild", 'serverinfo', 'si'])
    async def server(self, ctx):
        sid = ctx.guild.id
        owner = ctx.guild.owner.mention
        region = ctx.guild.region
        created = ctx.guild.created_at.strftime("%d/%m/%Y %I:%M:%S")
        members = len([i for i in ctx.guild.members if not i.bot])
        bots = len([i for i in ctx.guild.members if i.bot])
        members_offline = len([i for i in ctx.guild.members if i.status == discord.Status.offline])
        members_online = len([i for i in ctx.guild.members if i.status == discord.Status.online])
        members_idle = len(
            [i for i in ctx.guild.members if i.status == discord.Status.idle or i.status == discord.Status.dnd])
        def_channel = "#{}".format(ctx.guild.system_channel)
        afk = ctx.guild.afk_channel
        afk_time = "{} minutes".format(ctx.guild.afk_timeout / 60)
        text_channels = len(ctx.guild.text_channels)
        voice_channels = len(ctx.guild.voice_channels)
        channels = "`{}` Text | `{}` Voice | **{}** Total".format(text_channels, voice_channels,
                                                                  text_channels + voice_channels)
        roles = len(ctx.guild.roles)
        emotes = ''.join(map(str, ctx.guild.emojis))
        description = "**ID**: `{}`\n**Owner**: {}\n**Region**: __{}__\n**Created**: `{}` \n**Users**: `{}` Online | `{}`" \
                      " Away | `{}` Offline | **{}** Total(+{} bots)\n**Default Channel**: {}\n**AFK Channel**: #{}\n**AFK " \
                      "Timeout**: {}\n**Channels**: {}\n**Roles**: `{}`\n**Emojis**: {}".format(sid, owner, region,
                                                                                                created,
                                                                                                members_online,
                                                                                                members_idle,
                                                                                                members_offline,
                                                                                                members,
                                                                                                bots,
                                                                                                def_channel, afk,
                                                                                                afk_time,
                                                                                                channels, roles, emotes)

        embed = discord.Embed(title="🔍{}".format(ctx.guild.name), description=description, colour=0xb18dff)
        embed.set_thumbnail(url=ctx.guild.icon_url)
        await ctx.send(embed=embed)

    @commands.command(help="Get's servers icon", aliases=['serverimage', 'servericon'])
    async def simage(self, ctx):
        await ctx.send(ctx.guild.icon_url)

    @commands.command()
    async def roles(self, ctx, user: converters.FullMember = None):
        user = user or ctx.author
        roles = '\n'.join([x.name for x in user.roles][1:])
        embed = discord.Embed(title=f"{user.display_name}'s roles.", description=roles, colour=0xb18dff)
        embed.set_thumbnail(url=user.avatar_url)

        await ctx.send(embed=embed)

    @commands.command(aliases=["fb"], help="Send feedback to the bot author. \n`>feedback what you want to send here`")
    async def feedback(self, ctx, *, arg):
        user = ctx.bot.get_user(int(MooseBot.owner))
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

    @commands.command(aliases=['p', 'flee', 'market', 'price'])
    async def fleemarket(self, ctx, *, args):
        url = 'https://tarkov-market.com/api/v1/item?q='
        key = MooseBot.tarkovKey
        request = url + args + key
        try:
            response = requests.get(request)
            if response.status_code == 200:
                data = response.text
                if len(data) == 0:
                    await ctx.send("Cannot find item by that search term, please type the item name exactly.")
                    return
                parsed = json.loads(data)[0]
                date = datetime.datetime.strptime((parsed['updated']).replace('T', ' ').replace('Z', ''), '%Y-%m-%d %H:%M:%S.%f')
                #newdate = date + datetime.timedelta(hours=10)
                timesince = datetime.datetime.now() - date
                seconds = timesince.total_seconds()
                minutes = int((seconds % 3600) // 60)
                hours = int(seconds // 3600)
                lastupdated = f"Last updated {f'{hours} hours, ' if hours != 0 else ''}{minutes} minutes and {int(seconds % 60)} seconds ago."
                desc = f"🔹**Price:** {parsed['price']:,}₽\n" \
                       f"🔹**Trader Price:** {parsed['traderPrice']:,}{parsed['traderPriceCur']} ({parsed['traderName']})\n" \
                       f"🔹**Last Updated:** {lastupdated}\n" \
                       f"🔹**Average 24h Price:** ₽{parsed['avg24hPrice']:,}\n" \
                       f"🔹**Average 7day Price:** ₽{parsed['avg7daysPrice']:,}\n" \
                       f"🔹**Price Per Slot:** ₽{parsed['price'] / parsed['slots']:,}\n" \
                       f"🔹**Wiki Link:** {parsed['wikiLink']}"
                embed = discord.Embed(title=f"{parsed['name']} flee market information.", description=desc,
                                      colour=0xb18dff)
                embed.set_thumbnail(url=parsed['icon'])
                await ctx.send(embed=embed)

        except Exception:
            await ctx.send("Unable to process this request right now. Please try again.")

    @commands.command(aliases=['user', 'ui'], help="Provides information about a user. \n`>ui user`")
    async def userinfo(self, ctx, *, member: converters.FullMember = None):
        member = member or ctx.author
        member_date = datetime.date(member.created_at.year, member.created_at.month, member.created_at.day)
        age = datetime.date.today() - member_date
        roles = [f"`{i.name}`" for i in member.roles]
        isowner = ""
        if member == ctx.guild.owner:
            isowner = "👑__**Guild owner**__👑\n"
        description = f"{isowner}▫**User ID**: `{member.id}`\n▫**Join Date**: {member.joined_at.strftime('%d/%m/%Y')}\n" \
                      f"▫**Account Created**: {member.created_at.strftime('%d/%m/%Y')}\n▫**Account Age**: {age.days} days" \
                      f"\n▫**Voice Channel**: {member.voice.channel.name if member.voice else 'None'}\n▫**Playing Now**: " \
                      f"{'' if not member.activity else member.activity.name}\n▫**Colour**: {str(member.colour).upper()}\n▫**Status**: {str(member.status).title()}"
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
        embed.add_field(name="Author", value=f"<@{MooseBot.owner}>")
        embed.add_field(name='Contributors', value='<@702226595670261851>')
        embed.add_field(name="Server count", value=f"{len(self.bot.client.guilds)}")
        embed.add_field(name="Invite me to your server!",
                        value="[Invite link](https://discordapp.com/oauth2/authorize?client_id=445936072288108544&scope=bot&permissions=66186303)")
        embed.add_field(name="Join my server!", value="[Join here!](https://discord.gg/7Jcu6yn)")
        embed.add_field(name='Github', value='[Look at my trash code](https://github.com/SilverEyess/MooseBot)')
        embed.set_thumbnail(url=ctx.me.avatar_url)
        await ctx.send(embed=embed)

    @commands.command(aliases=['e', 'emj'])
    async def emoji(self, ctx, emoji: discord.Emoji):
        try:
            embed = discord.Embed(title=emoji.name, colour=0xb18dff)
            emj = emoji.guild.fetch_emoji
            # await ctx.send(emj.emoji)
            embed.set_image(url=emoji.url)
            await ctx.send(embed=embed)

        except Exception:
            await ctx.send("Currently I'm too dumb to fetch emoji's from servers I'm not in.")

    @commands.command(help="Provides bot invite link.")
    async def invite(self, ctx):
        embed = discord.Embed(title="Moosebot invite", description="Invite Moosebot to your server!", colour=0xb18dff)
        embed.add_field(name="Invite",
                        value="Invite me using this **[link](https://discordapp.com/oauth2/authorize?client_id=445936072288108544&scope=bot&permissions=66186303)**")
        embed.set_thumbnail(url=ctx.me.avatar_url)
        await ctx.send(embed=embed)

    @commands.command(help="This is literally the help command.", aliases=['h'])
    async def help(self, ctx, *, arg: str = None):
        from moosebot.cog_helper import get_cog_group

        if arg is None:
            embed = discord.Embed(title="MooseBot", description="A bot that copies other bots and is also a Moose.",
                                  colour=0xb18dff)

            commands = [(get_cog_group(self.bot.client, cog[0]), command)
                        for cog in [(name, self.bot.client.get_cog(name)) for name in self.bot.client.cogs]
                        if type(cog[1]) not in Info.ignored_cogs
                        for command in cog[1].get_commands()]

            groups = OrderedDict()

            for cog, command in commands:
                if command.hidden: continue
                if cog in groups:
                    groups[cog].append(command)
                else:
                    groups[cog] = [command]

            for cog, commands in groups.items():
                embed.add_field(name=cog,
                                value=" ".join([f"`{c.name}`" for c in commands]),
                                inline=False)

            embed.set_thumbnail(url=ctx.me.avatar_url_as(format='png'))
            embed.set_footer(text=f"{MooseBot.prefix}help [command] to get help for that command.")
            await ctx.send(embed=embed)
        else:
            try:
                command = self.bot.client.get_command(name=arg)
                if command.hidden:
                    await ctx.send(f"Command `{arg}` not found.")
                elif command.help:
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
                            embed = discord.Embed(title="City information.", description=description, colour=0xb18dff)
                            await ctx.send(embed=embed)
            except Exception:
                await ctx.send("I can't find this city cus I'm dumb.")


def setup(bot):
    bot.add_cog(Info(bot.moose))
