import asyncio
import random
import re
from typing import List, Any

import discord
from discord.ext import commands
from discord.ext.commands import Bot

from moosebot.utils import *


class MooseBot:
    prefix = ">"
    owners = [192519529417408512, 702226595670261851]

    def __init__(self, token):
        from moosebot import MooseDb

        self.phone_servers = []
        self.phone_channels = []

        self.token = token
        client = Bot(command_prefix=MooseBot.prefix)
        self.client = client
        self.client.moose = self
        self.database = MooseDb()
        self.db = self.database.db

        client.remove_command('help')

        @client.event
        async def on_ready():
            print("Logged in as {}({})".format(client.user.name, client.user.id))
            print("-----------------------------------------")

            await client.change_presence(activity=discord.Game(name=">cast a line and catch some fish!"))

        @client.event
        async def on_guild_join(guild):
            if guild.system_channel is not None:
                channel = guild.system_channel
            else:
                for c in guild.text_channels:
                    if not c.permissions_for(guild.me).send_messages:
                        continue
                    channel = c
            embed = discord.Embed(title="Thanks for inviting me! I am MooseBot.",
                                  description="I require admin permissions to fully function!", colour=0xb18dff)
            embed.add_field(name="Author", value="<@192519529417408512>")
            embed.add_field(name="Server count", value=f"{len(client.guilds)}")
            embed.add_field(name="Invite me to your server!",
                            value="[Invite link](https://discordapp.com/oauth2/authorize?client_id=445936072288108544&scope=bot&permissions=66186303)")
            embed.add_field(name="Join my server!", value="[Join here!](https://discord.gg/7Jcu6yn)")
            embed.set_thumbnail(url=guild.me.avatar_url_as(format='png'))
            await channel.send(embed=embed)
            self.database.db.lvl.insert_one({'serverid': str(guild.id)})
            self.database.db.xp.insert_one({'serverid': str(guild.id)})


        # @client.event
        # async def on_command_error(ctx, error):
        #     if isinstance(error, commands.CommandNotFound):
        #         print("{} is retarded and '{}' isn't a command.".format(ctx.author.display_name, ctx.message.content))

        @client.event
        async def on_member_join(member):
            winner = random.choice([i for i in member.guild.members if not i.bot]).mention
            choices = ("Welcome {}!", "{} has joined!", "{} is here to kick ass and chew bubblegum, "
                                                        "and we're all out of ass.", "Prepare yourselves, {} is here.",
                       "Pack your things, {} is here...", "{} has finally arrived.", "Ready player {}!",
                       "{} once promised me a bike, they never delivered.", "It's dangerous to go alone, take {}!",
                       "Hide the weed, {} is here!", "Party is over... {} showed up.",
                       "I thought {1} was lame, but now that {0} is here, I'm not sure.")

            server = await self.db.server.find_one({'serverid': str(member.guild.id)})
            await asyncio.gather(generate(str(member.id)))
            if server is None:
                await self.db.server.update_one({'serverid': str(member.guild.id)})
            elif 'welcomechannel' in server:
                welcome = client.get_channel(int(server['welcomechannel']))
                await welcome.send(random.choice(choices).format(member.mention, winner))
            else:
                return

        async def generate(user):

            people = self.db.money
            userid = user
            person = people.find_one({'userid': userid})
            if person is None:
                await people.update_one({'userid': userid}, {'$set': {'fish.totalweight': 0}})
                await people.update_one({'userid': userid}, {'$set': {'fish.largestfish': 0}})
                await people.update_one({'userid': userid}, {'$set': {'fish.recentfish': 0}})
                await people.update_one({'userid': userid}, {'$set': {'fish.totalfish': 0}})
                await people.update_one({'userid': userid}, {'$set': {'fish.sincelastsell': 0}})
                await people.update_one({'userid': userid}, {'$set': {'fish.rod': 'None'}})
                await people.update_one({'userid': userid}, {'$set': {'fish.curbait': 'None'}})
                await people.update_one({'userid': userid}, {'$set': {'fish.bait.Bait': 0}})
                await people.update_one({'userid': userid}, {'$set': {'fish.bait.Game Bait': 0}})
                await people.update_one({'userid': userid}, {'$set': {'balance': 0}})
                await people.update_one({'userid': userid}, {'$set': {'daily': 'None'}})
                await people.update_one({'userid': userid}, {'$set': {'weekly': 'None'}})
                await people.update_one({'userid': userid}, {'$push': {'inventory': 'Yeet'}})
                await people.update_one({'userid': userid}, {'$pull': {'inventory': 'Yeet'}})
            else:
                return

        @client.event
        async def on_member_remove(member):
            winner = random.choice([i for i in member.guild.members if not i.bot]).mention
            choices = ("{} is outta here.", "{} is gone.", "Cya later {}!", "{} left.", "Adios {}.", "Sayonara {}",
                       "Don't let the door hit you on the way out {}!", "{1} kicked {0} to a whole new server.",
                       "Finally {} is gone.", "It's about time {} left.", "Time to celebrate {} is gone", "Ciao {}!",
                       "auf Wiedersehen {}!", "Bon voyage {}.", "Shalom {}")
            server = await self.db.server.find_one({'serverid': str(member.guild.id)})
            if server is None:
                await self.db.server.update_one({'serverid': str(member.guild.id)})
            elif 'welcomechannel' in server:
                welcome = client.get_channel(int(server['welcomechannel']))
                await welcome.send(random.choice(choices).format(member.mention, winner))
            else:
                return

        @client.event
        async def on_message(message):
            if isinstance(message.channel, discord.abc.PrivateChannel):
                await asyncio.gather(self.senddm(message))
            else:
                ctx = await client.get_context(message)
                await asyncio.gather(
                    self.rad(message),
                    self.dar(message),
                    self.saveattach(message),
                    self.mobile(ctx),
                    self.what(ctx)
                )
            await client.process_commands(message)


        @client.event
        async def on_guild_join(guild):
            if guild.system_channel is not None:
                channel = guild.system_channel
            else:
                for c in guild.text_channels:
                    if not c.permissions_for(guild.me).send_messages:
                        continue
                    channel = c
            embed = discord.Embed(title="Thanks for inviting me! I am Moosebot.",
                                  description="I require admin permissions to fully function!", colour=0xb18dff)
            embed.add_field(name="Author", value="<@192519529417408512>")
            embed.add_field(name="Server count", value=f"{len(client.guilds)}")
            embed.add_field(name="Invite me to your server!",
                            value="[Invite link](https://discordapp.com/oauth2/authorize?client_id=445936072288108544&scope=bot&permissions=66186303)")
            embed.add_field(name="Join my server!", value="[Join here!](https://discord.gg/7Jcu6yn)")
            embed.set_thumbnail(url=guild.me.avatar_url_as(format='png'))
            await channel.send(embed=embed)
            self.database.db.lvl.insert_one({'serverid': str(guild.id)})
            self.database.db.xp.insert_one({'serverid': str(guild.id)})

    def launch(self, token):
        self.client.run(token)

    async def senddm(self, message):
        if message.guild is None:
            if message.author.id == 445936072288108544 or message.author.id == 192519529417408512:
                return
            else:
                me = self.client.get_user(192519529417408512)
                format = f"**{message.author.display_name}**({message.author.id}): `{message.content}`"
                await me.send(format)

    async def rad(self, message):
        dard = self.client.get_emoji(446703695204450305)
        if message.content == "<:rad:428937672552349698>":
            await message.add_reaction(dard)

    async def dar(self, message):
        radical = self.client.get_emoji(428937672552349698)
        if message.content == "<:dar:446703695204450305>":
            await message.add_reaction(radical)

    # async def saveattach(self, message):
    #     if message.author.id == self.client.user.id:
    #         return None
    #     else:
    #         channel = message.guild.get_channel(449821022846320641)
    #         if len(message.attachments) >= 1:
    #             path = "database/attachments"
    #             for i in message.attachments:
    #                 url = i.url
    #                 data = get_image(url)
    #                 file_name = str(i.id)
    #                 file_type = i.url[-4:]
    #                 types = [".png", ".mp4", ".jpg", ".gif", ".gifv", ".mp3", ".jpeg", ".mov"]
    #                 if file_type in types:
    #                     save_image(path, file_name, data, file_type)
    #                 else:
    #                     file_type = i.url[-5:]
    #                     if file_type in types:
    #                         save_image(path, file_name, data, file_type)
    #                     else:
    #                         file_type = ".png"
    #                         save_image(path, file_name, data, file_type)
    #                 file_type = i.url[-4:]
    #                 file_path = os.path.join(path, file_name + file_type)
    #                 await asyncio.sleep(2)
    #                 if message.guild.id == 427010987334434816:
    #                     await channel.send(file=discord.File(file_path))

    async def mobile(self, ctx):
        channel = ctx.channel
        if ctx.message.author.bot:
            return None
        elif ctx.message.content == ">phone":
            return None
        elif len(ctx.message.embeds) > 0:
            return None
        elif len(ctx.message.attachments) > 0:
            return None
        elif len(self.phone_channels) == 2:
            if channel == self.phone_channels[0]:
                await self.phone_channels[1].send("**{}**#{}: {}".format(ctx.message.author.name,
                                                                         ctx.message.author.discriminator,
                                                                         ctx.message.content))
            elif channel == self.phone_channels[1]:
                await self.phone_channels[0].send("**{}**#{}: {}".format(ctx.message.author.name,
                                                                         ctx.message.author.discriminator,
                                                                         ctx.message.content))

    async def what(self, ctx):
        m = ctx.message.content.lower()
        whatlist = ["what", "wat", "wot", "wut", "scuseme"]
        for wat in whatlist:
            if m.strip(' ?!') == wat:
                message2 = await ctx.channel.history(before=ctx.message, limit=1).next()
                if message2.author == ctx.message.author:
                    await ctx.send("Are you dumb or something?")
                elif len(message2.embeds) >= 1:
                    await ctx.send("Yeah I'm not sure what they said either.")
                else:
                    unbolded = re.sub(r"\*\*(.+?)\*\*", r"\1", message2.content)
                    message = f"{message2.author.display_name} said: **{unbolded.upper()}**"
                    if len(message) > 2000:
                        await ctx.send("Yeah I'm not sure what they said either.")
                    else:
                        await ctx.send(message)

    @staticmethod
    async def is_owner(ctx):
        if ctx.author.id in MooseBot.owners:
            return True
        else:
            await ctx.send("You do not have permissions to use this command!")

    @staticmethod
    async def is_admin(ctx):
        perm = ctx.author.permissions_in(ctx.channel)
        if perm.administrator or await MooseBot.is_owner(ctx):
            return True
        else:
            return False

    @staticmethod
    async def is_mod(ctx):
        perm = ctx.author.permissions_in(ctx.channel)
        if perm.kick_members or perm.ban_members or await MooseBot.is_admin(ctx):
            return True
        else:
            return False

    #
    # async def generate(self, userid):
    #     userid = str(userid.id)
    #     await self.db.money.update_one({'userid': userid}, {'$set': {'fish.totalweight': 0}})
    #     await self.db.money.update_one({'userid': userid}, {'$set': {'fish.largestfish': 0}})
    #     await self.db.money.update_one({'userid': userid}, {'$set': {'fish.recentfish': 0}})
    #     await self.db.money.update_one({'userid': userid}, {'$set': {'fish.totalfish': 0}})
    #     await self.db.money.update_one({'userid': userid}, {'$set': {'fish.sincelastsell': 0}})
    #     await self.db.money.update_one({'userid': userid}, {'$set': {'fish.rod': 'None'}})
    #     await self.db.money.update_one({'userid': userid}, {'$set': {'fish.curbait': 'None'}})
    #     await self.db.money.update_one({'userid': userid}, {'$set': {'fish.bait.Bait': 0}})
    #     await self.db.money.update_one({'userid': userid}, {'$set': {'fish.bait.Game Bait': 0}})
    #     await self.db.money.update_one({'userid': userid}, {'$set': {'balance': 0}})
    #     await self.db.money.update_one({'userid': userid}, {'$set': {'daily': 'None'}})
    #     await self.db.money.update_one({'userid': userid}, {'$set': {'weekly': 'None'}})
    #     await self.db.money.update_one({'userid': userid}, {'$push': {'inventory': 'Yeet'}})
    #     await self.db.money.update_one({'userid': userid}, {'$pull': {'inventory': 'Yeet'}})
