import random
import time

import motor.motor_asyncio
from PIL import ImageFilter, Image
from discord.ext import commands
from pymongo import MongoClient

from moosebot import MooseBot
from moosebot import converters
from moosebot.cogs import *
from moosebot.utils import *

mongo = MongoClient()
db2 = mongo.MooseBot
mclient = motor.motor_asyncio.AsyncIOMotorClient()
db = mclient.MooseBot

with open('database/token.txt') as f:
    token = f.readline()

moose = MooseBot(token)
client = moose.client
admins = ["192519529417408512", "345484068886020108"]


async def is_admin(ctx):
    perm = ctx.author.permissions_in(ctx.channel)
    if perm.administrator or await is_owner(ctx):
        return True
    else:
        return False


async def is_owner(ctx):
    if ctx.author.id == 192519529417408512:
        return True
    else:
        await ctx.send("You do not have permissions to use this command!")


async def is_mod(ctx):
    perm = ctx.author.permissions_in(ctx.channel)
    if perm.kick_members or perm.ban_members or await is_admin(ctx):
        return True
    else:
        return False


@client.event
async def on_ready():
    print("Logged in as {}({})".format(client.user.name, client.user.id))
    print("-----------------------------------------")

    await client.change_presence(game=discord.Game(name="Now with XP!"))


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
    db.lvl.insert_one({'serverid': str(guild.id)})
    db.xp.insert_one({'serverid': str(guild.id)})


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


def save(list, path):
    with open(path, 'w') as write_file:
        json.dump(list, write_file, indent=4)


def load(path):
    firstline = dict()
    if os.path.exists(path):
        with open(path, 'r') as read_file:
            data = json.load(read_file)
        return data
    else:
        s = json.dumps(firstline)
        with open(path, 'w+') as new_file:
            new_file.write(s)
            try:
                data = json.load(new_file)

            except json.JSONDecodeError:
                data = dict()
            return data


@client.command()
async def a(ctx):
    await ctx.send("A")


@client.command(help="This is literally the help command.", aliases=['h'])
async def help(ctx, *, arg: str = None):
    if arg is None:
        embed = discord.Embed(title="MooseBot", description="A bot that copies other bots and is also a Moose.",
                              colour=0xb18dff)
        embed.add_field(name="Fun Commands", value="`face` `guess` `8ball` `russian` `phone` `ping` `ship` `dadjoke` "
                                                   "`embarrass` `greek` `letters` `thicc` `choose` `cointoss` `roll` "
                                                   "`reverse` `rps` `urbandictionary` `translate` `square` `meme` "
                                                   "`clap`",
                        inline=False)
        embed.add_field(name='Experience', value='`level` `leaderboard`', inline=False)
        embed.add_field(name='Economy', value='`pay` `steal` `coinflip` `balance` `balancelb`', inline=False)
        embed.add_field(name="Info Commands", value="`server` `userinfo` `avatar` `bitcoin` `info` `invite` `emojis` "
                                                    "`gender` `inrole` `feedback`", inline=False)
        embed.add_field(name="Admin commands", value="`kick` `ban` `clear` `count` `nickname` `moveto`", inline=False)

        embed.set_thumbnail(url=ctx.me.avatar_url_as(format='png'))
        embed.set_footer(text=">help [command] to get help for that command.")
        await ctx.send(embed=embed)
    else:
        try:
            command = client.get_command(name=arg)
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


#
#
@client.command()
async def purge(ctx, where=None, limit=None):
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


#
#
# @client.command()
# async def calc(ctx, *, args):
#     dec = decimal.Context()
#     dec.prec = 40
#
#     def convert(f):
#         d1 = dec.create_decimal(repr(f))
#         return format(d1, 'f')
#
#     args = args.split(',')
#     args = ''.join(args)
#     e = int(float(convert(eval(args))))
#     await ctx.send(f'{e:,d}')
#
#
#
#
#
#

@client.command()
async def simage(ctx):
    await ctx.send(ctx.guild.icon_url)


@client.command(help="Enter an amount of messages to purge from the chat. \n`>clear amount`")
@commands.check(is_mod)
async def clear(ctx, amount: int = None):
    amount = amount or None
    if amount is None:
        amount = 1
    deleted = await ctx.channel.purge(limit=amount + 1)
    await ctx.send(f"I have cleared `{len(deleted)- 1}` messages.", delete_after=0.5)


@client.command()
@commands.check(is_owner)
async def hangup(ctx):
    if len(moose.phone_channels) == 2:
        for i in moose.phone_channels:
            await i.send("Owner forcibly hung up the phone to use it himself lmoa")
            await ctx.message.delete()
        del moose.phone_channels[:]
    else:
        await ctx.send("You idiot, the phone isn't being used rn")
        await ctx.message.delete()


@client.command(help="Calls another server on the phone.")
async def phone(ctx):
    channel = ctx.channel
    this_server = ctx.guild
    if len(moose.phone_channels) == 0:
        moose.phone_servers.append(this_server)
        moose.phone_channels.append(channel)
        await ctx.send("Calling on the phone")
        await ctx.message.delete()
    elif channel not in moose.phone_channels and len(moose.phone_channels) == 2:
        await ctx.message.delete()
        await ctx.send("The phone is currently in use. Please wait and try again later")
    elif channel == moose.phone_channels[0]:
        await ctx.send("Hanging up the phone")
        await moose.phone_channels[1].send("The other party hung up the phone, "
                                           "use the command again to start another call!")
        await ctx.message.delete()
        del moose.phone_channels[:]
    elif channel in moose.phone_channels:
        await ctx.send("Hanging up the phone")
        await moose.phone_channels[0].send("The other party hung up the phone, "
                                           "use the command again to start another call!")
        await ctx.message.delete()
        del moose.phone_channels[:]
    elif channel not in moose.phone_channels and len(moose.phone_channels) == 1:
        moose.phone_channels.append(channel)
        moose.phone_servers.append(this_server)
        await moose.phone_channels[0].send("You are now connected to someone through the phone, say hi!")
        await moose.phone_channels[1].send("You are now connected to someone through the phone, say hi!")


@client.command(help="Provide a user to sharpen their avatar or just an image to sharpen. Takes multiple passes to "
                     "have visible effect.")
async def sharpen(ctx, *args):
    full_path = "database/avatar/temp_image.png"
    path = "database/avatar/"
    file_name = "temp_image"
    if len(ctx.message.mentions) == 1:
        user_avatar = ctx.message.mentions[0].avatar_url_as(format='png')
        data = get_image(user_avatar)
        save_image(path, file_name, data)
        im = Image.open(full_path)
        im_sharp = im.filter(ImageFilter.SHARPEN)
        im_sharp.save("database/avatar/temp_image.png", "PNG")
        await ctx.send(file=discord.File('database/avatar/temp_image.png'))

    elif len(ctx.message.attachments) == 1:
        url = ctx.message.attachments[0].url
        data = get_image(url)
        save_image(path, file_name, data)
        im = Image.open(full_path)
        im_sharp = im.filter(ImageFilter.SHARPEN)
        im_sharp.save("database/avatar/temp_image.png", "PNG")
        await ctx.send(file=discord.File('database/avatar/temp_image.png'))

    elif len(args) == 1 and args[0].startswith('http'):
        url = args[0]
        try:
            print(args[0])
            data = get_image(url)
            save_image(path, file_name, data)
            im = Image.open(full_path)
            im_sharp = im.filter(ImageFilter.SHARPEN)
            im_sharp.save("database/avatar/temp_image.png", "PNG")
            await ctx.send(file=discord.File('database/avatar/temp_image.png'))
        except Exception:
            await ctx.send("That url is invalid for whatever reason")

    elif len(args) >= 1:
        memberlist = ctx.guild.members
        name = ' '.join(args)
        match = next(iter([x for x in iter(memberlist) if name.lower() == x.display_name.lower()]), None)
        if match is not None:
            match_index = memberlist.index(match)
            user_object = memberlist[match_index]
            user_url = user_object.avatar_url_as(format='png')
            data = get_image(user_url)
            save_image(path, file_name, data)
            im = Image.open(full_path)
            im_sharp = im.filter(ImageFilter.SHARPEN)
            im_sharp.save("database/avatar/temp_image.png", "PNG")
            await ctx.send(file=discord.File('database/avatar/temp_image.png'))

    else:
        im = Image.open(full_path)
        im_sharp = im.filter(ImageFilter.SHARPEN)
        im_sharp.save("database/avatar/temp_image.png", "PNG")
        await ctx.send(file=discord.File('database/avatar/temp_image.png'))


# @client.command()
# async def colourme(ctx, arg):
#     rolelist = ctx.author.roles
#     name = ctx.author.display_name
#     lowername = name.lower()
#     colour = discord.Colour(int("0x" + arg, 16))
#     for i in rolelist:
#         print(i)
#         if lowername == i.name.lower():
#             await i.edit(colour=colour)
#         else:
#             await ctx.send("You do not possess a role with this ability")


@client.command(help="Pong.")
async def ping(ctx):
    ptime = time.time()
    x = await ctx.send("Ok, pinging.")
    pingtime = (time.time() - ptime) * 100
    msg = f"It took {pingtime:.02f}ms to ping the Moose."
    await x.edit(content=msg)


@client.command(help="Get's a users avatar. \n`>avatar user`")
async def avatar(ctx, *, member: converters.FullMember = None):
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


#
#


#
#
#
#
#
#
#
#

#


#
#
# @client.command(help="Change the bots current game. BOT OWNER ONLY.")
# @commands.check(is_owner)
# async def botgame(ctx, *args):
#     game_name = ' '.join(args)
#     game = discord.Game(name=game_name)
#     if await client.change_presence(game=game):
#         await ctx.message.delete()
#
#
# @client.command(help="Kicks user. \n`>kick user`")
# @commands.check(is_mod)
# async def kick(ctx):
#     this_server = ctx.guild
#     if len(ctx.message.mentions) == 0:
#         await ctx.send("Please mention a user to kick")
#     elif ctx.message.mentions[0] == ctx.message.author:
#         await ctx.send("You cannot kick yourself.")
#     elif len(ctx.message.mentions) == 1:
#         user = ctx.message.mentions[0]
#         if user.id == 192519529417408512:
#             await ctx.send('You cannot kick Daddy dear.')
#         else:
#             try:
#                 await this_server.kick(user=user)
#                 await ctx.send("{} was successfully kicked".format(ctx.message.mentions[0].display_name))
#             except discord.Forbidden:
#                 await ctx.send("I don't have sufficient permissions to kick")
#             else:
#                 try:
#                     await this_server.kick(user=user)
#                 except discord.HTTPException:
#                     await ctx.send("You do not have permission to kick users.")
#     elif len(ctx.message.mentions) > 1:
#         await ctx.send("Please only mention one user at a time")
#
#
# @client.command(help="Bans user. \n`>ban user`")
# @commands.check(is_mod)
# async def ban(ctx):
#     this_server = ctx.guild
#     if len(ctx.message.mentions) == 0:
#         await ctx.send("Please mention a user to ban")
#     elif ctx.message.mentions[0] == ctx.message.author:
#         await ctx.send("You cannot ban yourself.")
#     elif len(ctx.message.mentions) == 1:
#         user = ctx.message.mentions[0]
#         if user.id == 192519529417408512:
#             await ctx.send('You cannot ban Daddy dear.')
#         else:
#             try:
#                 await this_server.ban(user=user)
#                 await ctx.send("{} was successfully banned".format(ctx.message.mentions[0].display_name))
#             except discord.Forbidden:
#                 await ctx.send("I don't have sufficient permissions to ban")
#             else:
#                 try:
#                     await this_server.ban(user=user)
#                 except discord.HTTPException:
#                     await ctx.send("You do not have permission to ban users.")
#     elif len(ctx.message.mentions) > 1:
#         await ctx.send("Please only mention one user at a time")
#
#
# @client.command(pass_context=True, help="Returns information about this bot.")
# async def info(ctx):
#     embed = discord.Embed(title="MooseBot", description="This bot a moose.", colour=0xb18dff)
#     embed.add_field(name="Author", value="<@192519529417408512>")
#     embed.add_field(name='Contributors', value='<@488682312154742787>')
#     embed.add_field(name="Server count", value=f"{len(client.guilds)}")
#     embed.add_field(name="Invite me to your server!",
#                     value="[Invite link](https://discordapp.com/oauth2/authorize?client_id=445936072288108544&scope=bot&permissions=66186303)")
#     embed.add_field(name="Join my server!", value="[Join here!](https://discord.gg/7Jcu6yn)")
#     embed.add_field(name='Github', value='[Look at my trash code](https://github.com/SilverEyess/MooseBot)')
#     embed.set_thumbnail(url=ctx.me.avatar_url)
#     await ctx.send(embed=embed)
#
#
# @client.command(help="Provides bot invite link.")
# async def invite(ctx):
#     embed = discord.Embed(title="Moosebot invite", description="Invite Moosebot to your server!", colour=0xb18dff)
#     embed.add_field(name="Invite",
#                     value="Invite me using this **[link](https://discordapp.com/oauth2/authorize?client_id=445936072288108544&scope=bot&permissions=66186303)**")
#     embed.set_thumbnail(url=ctx.me.avatar_url)
#     await ctx.send(embed=embed)
#
#
# @client.command(name="RussianRoulette",
#                 aliases=["rr", "russian"], help="Enter a phrase/word to award it to a random member. \n`>rr phrase`")
# async def russian(ctx, *args):
#     roulette = ' '.join(args[:])
#     winner = random.choice([i for i in ctx.guild.members if not i.bot])
#
#     if len(args) == 0:
#         await ctx.send("Please enter text to use this command")
#     else:
#         await ctx.send("And the winner of `{}` is {}.".format(roulette, winner.mention))
#
#
#
#
# @client.command(help="Ships 2 things together, can be a mix of words and mentions/users. \n`>ship item1 item2`")
# async def ship(ctx, arg1: MemberDisplayname, *, arg2: MemberDisplayname):
#     if arg1 == arg2:
#         await ctx.send(arg1)
#     else:
#         ship_str = random.randint(0, 100)
#         name1_len = int(len(arg1) / 2)
#         name2_len = int(len(arg2) / 2)
#         name1 = arg1[:name1_len].strip()
#         name2 = arg2[name2_len:].strip()
#
#         if ship_str == 100:
#             embed = discord.Embed(title=f"Ship name: {name1}{name2}", description=None, colour=0xb18dff)
#             embed.add_field(name="Compatibility", value=f"{ship_str}% [##########] Y'all should fuck! 💗")
#         elif ship_str >= 90:
#             embed = discord.Embed(title=f"Ship name: {name1}{name2}", description=None, colour=0xb18dff)
#             embed.add_field(name="Compatibility.", value=f"{ship_str}% [#########-] Great match!")
#         elif ship_str >= 80:
#             embed = discord.Embed(title=f"Ship name: {name1}{name2}", description=None, colour=0xb18dff)
#             embed.add_field(name="Compatibility.", value=f"{ship_str}% [########--] Good match.")
#         elif ship_str >= 70:
#             embed = discord.Embed(title=f"Ship name: {name1}{name2}", description=None, colour=0xb18dff)
#             embed.add_field(name="Compatibility.", value=f"{ship_str}% [#######---] Good match.")
#         elif ship_str >= 60:
#             embed = discord.Embed(title=f"Ship name: {name1}{name2}", description=None, colour=0xb18dff)
#             embed.add_field(name="Compatibility.", value=f"{ship_str}% [######----] Okay match.")
#         elif ship_str >= 50:
#             embed = discord.Embed(title=f"Ship name: {name1}{name2}", description=None, colour=0xb18dff)
#             embed.add_field(name="Compatibility.", value=f"{ship_str}% [#####-----] Okay match.")
#         elif ship_str >= 40:
#             embed = discord.Embed(title=f"Ship name: {name1}{name2}", description=None, colour=0xb18dff)
#             embed.add_field(name="Compatibility.", value=f"{ship_str}% [####------] Barely a thing.")
#         elif ship_str >= 30:
#             embed = discord.Embed(title=f"Ship name: {name1}{name2}", description=None, colour=0xb18dff)
#             embed.add_field(name="Compatibility.", value=f"{ship_str}% [###-------] Barely a thing.")
#         elif ship_str >= 20:
#             embed = discord.Embed(title=f"Ship name: {name1}{name2}", description=None, colour=0xb18dff)
#             embed.add_field(name="Compatibility.", value=f"{ship_str}% [##--------] Don't even try.")
#         elif ship_str >= 10:
#             embed = discord.Embed(title=f"Ship name: {name1}{name2}", description=None, colour=0xb18dff)
#             embed.add_field(name="Compatibility.", value=f"{ship_str}% [#---------] This is awful.")
#         elif ship_str >= 10:
#             embed = discord.Embed(title=f"Ship name: {name1}{name2}", description=None, colour=0xb18dff)
#             embed.add_field(name="Compatibility.", value=f"{ship_str}% [#---------] Just stop.")
#         else:
#             embed = discord.Embed(title=f"Ship name: {name1}{name2}", description=None, colour=0xb18dff)
#             embed.add_field(name="Compatibility.", value=f"{ship_str}% [----------] No.")
#
#         await ctx.send(f"💜`{arg1}`\n💜`{arg2}`")
#         await ctx.send(embed=embed)
#
#
# @client.command()
# @commands.check(is_owner)
# async def leavesvr(ctx, sid):
#     this_server = client.get_guild(int(sid))
#     await this_server.leave()
#     await ctx.send("Leaving {} Guild".format(sid))
#     await ctx.message.delete()
#
#
#
#
# @client.command()
# async def testp(ctx, url):
#     voice_channel = ctx.author.voice.channel
#     opts = {
#         'format': 'bestaudio/best',
#         'postprocessors': [{
#             'key': 'FFmpegExtractAudio',
#             'preferredcodec': 'mp3',
#             'preferredquality': '192'
#         }]
#     }
#
#     # Check that user is in voice channel
#     if ctx.author.voice.channel is not None:
#
#         # Check if already a voice client
#         if ctx.guild.voice_client is not None:
#             # if there is, add song to queue
#             pass
#
#         # if there isn't create one
#         elif ctx.guild.voice_client is None:
#             # join VC
#             vc = await voice_channel.connect(timeout=60, reconnect=True)
#         # Check that is valid url
#         if url.startswith("https://www.youtube.com/watch?v="):
#
#             # Get video information and store in song_info, with video source as url
#             with youtube_dl.YoutubeDL(opts) as ydl:
#                 song_info = ydl.extract_info(url, download=False)
#                 url = song_info['url']
#                 # play audio
#
#             vc.play(discord.FFmpegPCMAudio(url))
#             embed = discord.Embed(title="Now playing", description="[{}]({}) [{}]".format(song_info['title'], url,
#                                                                                           ctx.author.mention))
#             await ctx.send(embed=embed)
#
#             # display now playing
#
#         # If not, ask for valid url
#         else:
#             await ctx.send("Please enter a valid Youtube URL.")
#
#     # If not in a voice channel, ask user to join one
#     else:
#         await ctx.send("Please join a voice channel")
#
#
# async def check_con(ctx):
#     vcs = [i.guild for i in client.voice_clients]
#     if ctx.guild in vcs:
#         return True
#     else:
#         return False
#
#
# @client.command(help="Gets me to join your voice channel.")
# async def join(ctx):
#     voice_channel = ctx.author.voice.channel
#     await voice_channel.connect()
#
#
# @client.command(help="Gets me to leave your voice channel.")
# async def leave(ctx):
#     for x in client.voice_clients:
#         if x.guild == ctx.message.guild:
#             return await x.disconnect()
#
#     return await ctx.send("\u200BI am not connected to any voice channel on this server!")
#
#


def get_html(name):
    url = "https://www.stormshield.one/pve/stats/{}".format(name)
    response = requests.get(url)
    return response.text


@client.command(help="Returns my gender.")
async def gender(ctx):
    await ctx.send("I'm a boy, how could you not tell?")


def load_embarrass(path):
    embarrass_list = []
    with open(path, "r") as f:
        for entry in f.readlines():
            embarrass_list.append(entry.rstrip())
    return embarrass_list


def save_embarrass(path, embarrass_list):
    with open(path, "w") as f:
        for entry in embarrass_list:
            f.write(entry + "\n")


@client.command(aliases=["emb"], help="Embarrasses you or a friend! \n`>embarrass` \n`>embarrass user`")
async def embarrass(ctx, arg: converters.PartialMember = None, *, args=None):
    path = "database/embarrass.txt"
    embarrass_list = load_embarrass(path)
    bottle = client.get_user(192519529417408512)
    arg = arg or None
    args = args or None
    if arg is None:
        try:
            hook = await ctx.channel.create_webhook(name="Dadhook", avatar=None)
            await hook.send(content=random.choice(embarrass_list), username=ctx.author.display_name.ljust(2, '.'),
                            avatar_url=ctx.author.avatar_url)
            await hook.delete()
        except discord.Forbidden:
            await ctx.send("I require the manage webhooks permission for this command to function.")
    elif isinstance(arg, discord.Member):
        try:
            hook = await ctx.channel.create_webhook(name="Dadhook", avatar=None)
            await hook.send(content=random.choice(embarrass_list), username=arg.display_name.ljust(2, ','),
                            avatar_url=arg.avatar_url)
            await hook.delete()
        except discord.Forbidden:
            await ctx.send("I require the manage webhooks permission for this command to function.")
    elif arg.lower() == "add" or arg.lower() == "a":
        if args is None:
            await ctx.send("You need to enter a phrase to suggest being added to the embarrass list.")
        else:

            await ctx.send(f"{bottle.mention} add this phrase to the embarrass list? Y/N \n\n `{args}`")

            def check(m):
                return m.content.lower() == "yes" or m.content.lower() == "y" or m.content.lower() == "no" or m.content.lower() == "n" and m.author.id == 192519529417408512

            try:
                msg = await client.wait_for('message', check=check, timeout=10)
                if msg.content.lower() == 'yes' or msg.content.lower() == 'y':
                    await ctx.send("Adding phrase to embarrass list.")
                    embarrass_list.append(args)
                    save_embarrass(path, embarrass_list)
                elif msg.content.lower() == 'no' or msg.content.lower() == 'n':
                    await ctx.send(f"Your phrase has been denied {ctx.author.mention}")

            except asyncio.TimeoutError:
                await ctx.send("Daddy didn't respond in time, try again later.")
    elif arg.lower() == "del" or arg.lower() == "delete" or arg.lower() == "d":
        if args is None:
            await ctx.send("You need to enter a phrase to suggest being deleted from the embarrass list.")
        else:
            match = next(iter([x for x in iter(embarrass_list) if x.lower() == args.lower()]), None)
            if match is None:
                await ctx.send("That phrase was not found in the embarrass list.")
            else:
                await ctx.send(f"{bottle.mention} remove this phrase from the embarrass list? Y/N \n\n `{args}`")

                def check(m):
                    return m.content.lower() == "yes" or m.content.lower() == "y" or m.content.lower() == "no" or m.content.lower() == "n" and m.author.id == 192519529417408512

                try:
                    msg = await client.wait_for('message', check=check, timeout=10)
                    if msg.content.lower() == 'y' or msg.content.lower() == 'yes':
                        await ctx.send("Removing the phrase from the embarras list.")
                        embarrass_list.remove(match)
                        save_embarrass(path, embarrass_list)
                    elif msg.content.lower() == 'n' or msg.content.lower() == 'no':
                        await ctx.send("Your suggestion to remove that phrase has been denied {ctx.author.mention}")

                except asyncio.TimeoutError:
                    await ctx.send("Daddy didn't respond in time, try again later.")
    elif arg.lower() == 'l' or arg.lower() == 'list':
        embed = discord.Embed(title="Embarrassing phrases", description='\n'.join(embarrass_list))
        await ctx.send(embed=embed)
    else:
        await ctx.send("That's not an option for this command")


@client.command(aliases=["eightball", "8", "ball", "8ball"], help="Simple 8ball, ask a yes/no question and I'll tell "
                                                                  "you the outcome. \n`>8ball question`")
async def eight_ball(ctx):
    possible_responses = [
        "That's a no from me",
        "Big fat maybe",
        "I honestly can't be bothered answering",
        "Yeah, why not?",
        "Yes imo",
    ]
    await ctx.send(random.choice(possible_responses) + ", " + ctx.message.author.mention)


@client.command(aliases=["sqr"], help="Squares a number. \n`>square number`")
async def square(ctx, number):
    squared_value = float(number) * float(number)
    await ctx.send(str(number) + " squared is " + str(squared_value))


@client.command(aliases=["btc"], help="Returns the current price of bitcoin.")
async def bitcoin(ctx):
    url = "https://api.coindesk.com/v1/bpi/currentprice/BTC.json"
    response = requests.get(url)
    value = response.json()["bpi"]["USD"]["rate"]
    await ctx.send("Bitcoin price is: $" + value)


client.add_cog(Pet(moose))
client.add_cog(Shop(moose))
client.add_cog(Economy(moose))
# TODO rewrite
# client.add_cog(Experience(moose))
client.add_cog(Info(client))
client.add_cog(Counting(moose))
client.add_cog(Fun(moose))
client.add_cog(GuessGame(moose))
client.add_cog(Dad(moose))
client.add_cog(Moderation(moose))
client.add_cog(Server(moose))
client.run(token)
