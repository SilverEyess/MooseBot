import random

from discord.ext import commands
from discord.ext.commands import Bot

from moosebot.tasks import *


class MooseBot:
    prefix = ">"
    owners = [192519529417408512, 495151300821123072]

    def __init__(self, token):
        from moosebot import MooseDb

        self.phone_servers = []
        self.phone_channels = []

        self.token = token
        client = Bot(command_prefix=MooseBot.prefix)
        self.client = client
        self.database = MooseDb()

        client.remove_command('help')

        @client.event
        async def on_ready():
            print("Logged in as {}({})".format(client.user.name, client.user.id))
            print("-----------------------------------------")

            await self.client.change_presence(game=discord.Game(name="Now with XP!"))

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

        @client.event
        async def on_member_update(before, after):
            if after.guild.id == 377218458108035084:
                if after.id == 389579708016099328:
                    if after.display_name != "edgy baby":
                        await after.edit(nick="edgy baby")
                        print("Nat tried to change her nickname lmoa")
                # elif after.id == 488199047874740235:
                #     if after.display_name != 'anna':
                #         await after.edit(nick='anna')
                #         print('Anna tried to change her nickname.')
            else:
                return None

        @client.event
        async def on_command_error(ctx, error):
            if isinstance(error, commands.CommandNotFound):
                print("{} is retarded and '{}' isn't a command.".format(ctx.author.display_name, ctx.message.content))

        @client.event
        async def on_member_join(member):
            channel = client.get_channel(427012525998211072)
            winner = random.choice([i for i in member.guild.members if not i.bot]).mention
            choices = ("Welcome {}!", "{} has joined!", "{} is here to kick ass and chew bubblegum, "
                                                        "and we're all out of ass.", "Prepare yourselves, {} is here.",
                       "Pack your things, {} is here...", "{} has finally arrived.", "Ready player {}!",
                       "{} once promised me a bike, they never delivered.", "It's dangerous to go alone, take {}!",
                       "Hide the weed, {} is here!", "Party is over... {} showed up.",
                       "I thought {1} was lame, but now that {0} is here, I'm not sure.")

            if member.guild.id == 427010987334434816:
                await channel.send(random.choice(choices).format(member.mention, winner))

        @client.event
        async def on_member_remove(member):
            channel = client.get_channel(427012525998211072)
            winner = random.choice([i for i in member.guild.members if not i.bot]).mention
            choices = ("{} is outta here.", "{} is gone.", "Cya later {}!", "{} left.", "Adios {}.", "Sayonara {}",
                       "Don't let the door hit you on the way out {}!", "{1} kicked {0} to a whole new server.",
                       "Finally {} is gone.", "It's about time {} left.", "Time to celebrate {} is gone", "Ciao {}!",
                       "auf Wiedersehen {}!", "Bon voyage {}.", "Shalom {}")
            if member.guild.id == 427010987334434816:
                await channel.send(random.choice(choices).format(member.mention, winner))

        @client.event
        async def on_message(message):
            if isinstance(message.channel, discord.abc.PrivateChannel):
                await asyncio.gather(self.senddm(message))
            else:
                ctx = await client.get_context(message)
                await asyncio.gather(
                    rad(self, message),
                    dar(self, message),
                    saveattach(self, message),
                    mobile(self, ctx),
                    what(ctx)
                )
                if message.guild.id == 377218458108035084:
                    if message.content.startswith('ᵘʷᵘ oh frick ᵘʷᵘ ᵘʷᵘ') or message.content.endswith('ᵘʷᵘ ᵘʷᵘ sorry.'):
                        await message.delete()

            await client.process_commands(message)

    async def senddm(self, message):
        if message.guild is None:
            if message.author.id == 445936072288108544 or message.author.id == 192519529417408512:
                return
            else:
                me = self.client.get_user(192519529417408512)
                format = f"**{message.author.display_name}**({message.author.id}): `{message.content}`"
                await me.send(format)

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
