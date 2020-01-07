from discord.ext import commands
from discord.ext.commands import Cog

from moosebot import MooseBot, cog_group


@cog_group("Interactive")
class Phone(Cog):

    def __init__(self, bot: MooseBot):
        self.bot = bot

    @commands.command(hidden=True)
    @commands.check(MooseBot.is_owner)
    async def hangup(self, ctx):
        if len(self.bot.phone_channels) == 2:
            for i in self.bot.phone_channels:
                await i.send("Owner forcibly hung up the phone to use it himself lmoa")
                await ctx.message.delete()
            del self.bot.phone_channels[:]
        else:
            await ctx.send("You idiot, the phone isn't being used rn")
            await ctx.message.delete()

    @commands.command(help="Calls another server on the phone.")
    async def phone(self, ctx):
        channel = ctx.channel
        this_server = ctx.guild
        if len(self.bot.phone_channels) == 0:
            self.bot.phone_servers.append(this_server)
            self.bot.phone_channels.append(channel)
            await ctx.send("Calling on the phone")
            await ctx.message.delete()
        elif channel not in self.bot.phone_channels and len(self.bot.phone_channels) == 2:
            await ctx.message.delete()
            await ctx.send("The phone is currently in use. Please wait and try again later")
        elif channel == self.bot.phone_channels[0]:
            await ctx.send("Hanging up the phone")
            await self.bot.phone_channels[1].send("The other party hung up the phone, "
                                                  "use the command again to start another call!")
            await ctx.message.delete()
            del self.bot.phone_channels[:]
        elif channel in self.bot.phone_channels:
            await ctx.send("Hanging up the phone")
            await self.bot.phone_channels[0].send("The other party hung up the phone, "
                                                  "use the command again to start another call!")
            await ctx.message.delete()
            del self.bot.phone_channels[:]
        elif channel not in self.bot.phone_channels and len(self.bot.phone_channels) == 1:
            self.bot.phone_channels.append(channel)
            self.bot.phone_servers.append(this_server)
            await self.bot.phone_channels[0].send("You are now connected to someone through the phone, say hi!")
            await self.bot.phone_channels[1].send("You are now connected to someone through the phone, say hi!")


def setup(bot):
    bot.add_cog(Phone(bot.moose))
