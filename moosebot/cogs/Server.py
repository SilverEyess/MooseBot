import discord
from discord.ext import commands

from moosebot import MooseBot


class Server:

    def __init__(self, bot: MooseBot):
        self.bot = bot

    @commands.command()
    async def listsvr(self, ctx):
        embed = discord.Embed(title="Connected servers", description="List of servers that Moosebot is in.",
                              colour=0xb18dff)
        for i in self.bot.client.guilds:
            embed.add_field(name=i.name, value="**ID**: `{}`".format(i.id), inline=False)
        await ctx.send(embed=embed)

    @commands.command(help="Returns all emojis on this server")
    async def emojis(self, ctx):
        emojisl = []
        for i in ctx.guild.emojis:
            if i.animated:
                emojisl.append("<a:{}:{}> `:{}:` \n".format(i.name, i.id, i.name))
            else:
                emojisl.append("<:{}:{}> `:{}:` \n".format(i.name, i.id, i.name))
        emoji_list = ''.join(emojisl)
        await ctx.send(emoji_list)

    @commands.command(help="Returns information about this guild.", aliases=["guild"])
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
