import asyncio
import random
import shutil
import requests
from discord.ext.commands import Bot
import discord
from discord.ext import commands
import os
import datetime
import youtube_dl
from PIL import Image, ImageFilter
import time
from googletrans import Translator
from googletrans import LANGUAGES
import praw
import json

BOT_PREFIX = ">"
TOKEN = 'OMITTED'
client = Bot(command_prefix=BOT_PREFIX)
admins = ["192519529417408512", "345484068886020108"]
phone_server_list = []
phone_channel_list = []
client.remove_command('help')


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


# @client.event
# async def on_command_error(ctx, error):
#     if isinstance(error, commands.CommandNotFound):
#         print("{} is retarded and '{}' isn't a command.".format(ctx.author.display_name, ctx.message.content))

def save(self, list, path):
    with open(path, 'w') as write_file:
        json.dump(list, write_file, indent=4)

def load(self, path):
    firstline = dict()
    if os.path.exists(path):
        with open(path, 'r') as read_file:
            data = json.load(read_file)
        return data
    else:
        s = json.dumps(firstline)
        with open(path, 'w+') as new_file:
            new_file.write(s)
            data = json.load(new_file)
        return data


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
    # xp_list = load(f'database/experience/experience_{str(member.guild.id)}.json')
    # level_list = load(f'database/experience/levels_{str(member.guild.id)}.json')
    # if str(member.id) in xp_list:
    #     del xp_list[str(member.id)]
    # if str(member.id) in level_list:
    #     del level_list[str(member.id)]
    if member.guild.id == 427010987334434816:
        await channel.send(random.choice(choices).format(member.mention, winner))


@client.event
async def on_message(message):
    if isinstance(message.channel, discord.abc.PrivateChannel):
        await asyncio.gather(senddm(message))
    else:
        ctx = await client.get_context(message)
        await asyncio.gather(rad(message), dar(message), saveattach(message), mobile(ctx), what(ctx))
        if message.guild.id == 377218458108035084:
            if message.content.startswith('ᵘʷᵘ oh frick ᵘʷᵘ ᵘʷᵘ') or message.content.endswith('ᵘʷᵘ ᵘʷᵘ sorry.'):
                await message.delete()

    await client.process_commands(message)


async def senddm(message):
    if message.guild is None:
        if message.author.id == 445936072288108544 or message.author.id == 192519529417408512:
            return
        else:
            me = client.get_user(192519529417408512)
            format = f"**{message.author.display_name}**({message.author.id}): `{message.content}`"
            await me.send(format)


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


class Url_convert(commands.Converter):
    async def convert(self, ctx, arg):
        if arg.startswith("www."):
            arg = "https://" + arg
            return arg
        elif not arg.startswith("http://www."):
            arg = "http://www." + arg
            if not arg.endswith(".com") and not arg.endswith(".net") and not arg.endswith(".org"):
                arg = arg + ".com"
                return arg
            else:
                return arg
        elif not arg.endswith(".com") and not arg.endswith(".net") and not arg.endswith(".org"):
            arg = arg + ".com"
            return arg


class VoiceChannel(commands.Converter):

    async def convert(self, ctx, argument):
        try:
            arg = await commands.VoiceChannelConverter().convert(ctx, argument)
            return arg
        except commands.BadArgument:
            arg = [i for i in ctx.guild.voice_channels if
                   i.name.lower() == argument.lower()]
            if len(arg) >= 1:
                return arg[0]
            else:
                arg = [i for i in ctx.guild.voice_channels if
                       i.name.lower().startswith(argument.lower())]
                if len(arg) >= 1:
                    return arg[0]
                else:
                    return argument


@client.command()
async def purge(ctx, where=None, limit=None):
    limit = limit or None
    where = where or None
    if where is None:
        await ctx.send("You've got to give me something to work with here. Tell me where to delete(server/channel) then how many messages.")
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


class Fun:
    def __init__(self, bot):
        self.client = bot

    @commands.command(help="Clap👏to👏your👏text.")
    async def clap(self, ctx, *args):
        clapped = '👏'.join(args)
        await ctx.send(clapped)

    @commands.command(help="Returns a random spicy maymay.")
    async def meme(self, ctx):
        reddit = praw.Reddit(client_id="pok5Y9XHfdwYcA", client_secret="rnch9ufFK2nDpM75NhiDCKzZG_c",
                             user_agent="SilverEyes_")
        memes = [i for i in reddit.subreddit('dankmemes').hot(limit=100)]
        meme = random.choice(memes[1:])
        embed = discord.Embed(title=meme.title, description=f"[Image]({meme.url})", colour=0xb18dff)
        embed.set_image(url=meme.url)
        await ctx.send(embed=embed)

    @commands.command(aliases=['trans', 'gt'], help="This command will translate text. Provide a language as the first "
                                                    "argument to translate **TO** that language. Otherwise just enter "
                                                    "your text and it will translate to English.")
    async def translate(self, ctx, arg1, *, arg2=None):
        google_languages = LANGUAGES
        google_languages_reverse = {v: k for k, v in google_languages.items()}
        custom_languages = {
            "baguette": "french",
            "chink": "zh-cn",
            "gook": "zh-tw",
            "paki": "urdu",
            "indian": "hindi",
            "swampgerman": "dutch"

        }
        translator = Translator()
        if arg1.lower() in google_languages or arg1.lower() in google_languages_reverse:
            if arg2 is None:
                translated_text = translator.translate(arg1)
                embed = discord.Embed(title="MooseBot Translator.", description=f"Input text: `{arg1}`",
                                      colour=0xb18dff)
                embed.add_field(name=f"Translated from **English** to **English**:",
                                value=f"{translated_text.text}")
            else:
                translated_text = translator.translate(arg2, dest=arg1)
                embed = discord.Embed(title="MooseBot Translator.", description=f"Input text: `{arg2}`",
                                      colour=0xb18dff)
                embed.add_field(
                    name=f"Translated from **English** to **{arg1.title() if arg1 in google_languages_reverse else google_languages[arg1].title()}**:",
                    value=f"{translated_text.text}")
            await ctx.send(embed=embed)
        elif arg1.lower() in custom_languages:
            translated_text = translator.translate(arg2, dest=custom_languages[arg1])
            embed = discord.Embed(title="MooseBot Translator.", description=f"Input text: `{arg2}`", colour=0xb18dff)
            embed.add_field(name=f"Translated from **English** to **{arg1.title()}**:", value=f"{translated_text.text}")
            await ctx.send(embed=embed)
        else:
            if arg2 is None:
                input_text = str(arg1)
            else:
                input_text = str(arg1) + " " + str(arg2)
            translated_text = translator.translate(input_text)
            if translated_text.src in google_languages:
                language = google_languages[translated_text.src].title()
            elif translated_text.src in google_languages_reverse:
                language = google_languages_reverse[translated_text.src].title()
            embed = discord.Embed(title="MooseBot Translator.", description=f"Input text: `{input_text}`",
                                  colour=0xb18dff)
            embed.add_field(
                name=f"Translated from **{google_languages[translated_text.src.lower()].title() if translated_text.src.lower() in google_languages else google_languages_reverse[translated_text.src.lower()].title()}** to English:",
                value=f"{translated_text.text}")
            await ctx.send(embed=embed)

    @commands.command(help="Enter phrases/words separated by commas(,) and I will choose one at random.")
    async def choose(self, ctx, *choices: str):
        choices = ' '.join(choices)
        choices = choices.split(',')
        choice = random.randint(0, len(choices))
        if len(choices) == 1:
            await ctx.send("Please separate the choices with a comma `>choose a, b, c`.")
        else:
            await ctx.send(f"I choose `{choices[choice]}`.")

    @commands.command(help="Returns a random face.")
    async def face(self, ctx):
        choices = ("🌚 👅 🌚", "🌐➖🌐", "<:eye_in_speech_bubble:463956840905048066> ♨ "
                                        "<:eye_in_speech_bubble:463956840905048066>", "🌕 ♨ 🌕", "┌( ಠ_ಠ)┘",
                   "^-^", "OwO", "👌 👅 👌", "👅 👁 👅", "◔ ⌣ ◔", "◔̯◔",
                   "<:wobo:461535897666584586> ➖ <:wobo:461535897666584586>", "⭕〰⭕", "⭕ 💋 ⭕", "ง ͠° ل͜ °)ง", "๏̯͡๏﴿",
                   "༼ ºººººل͟ººººº ༽", "༼ つ ◕_◕ ༽つ", "༼ʘ̚ل͜ʘ̚༽", "ლ(´ڡ`ლ)", "ლ(́◉◞౪◟◉‵ლ)", "ლ(ಠ益ಠლ)", "╚(ಠ_ಠ)=┐",
                   "<:fat:428937630009262090> ➖ <:fat:428937630009262090>", "✌(-‿-)✌", "\_(ʘ_ʘ)_/", "ʕ•ᴥ•ʔ", "- o -",
                   "o - o", "ಠ▃ಠ", "ಠ╭╮ಠ", "ಥ_ಥ", "ಥ◡ಥ", "ಥ﹏ಥ", "ಥдಥ", ">﹏>", ">﹏<", "<﹏<", "༼ つ  >﹏<༽つ")
        await ctx.send(random.choice(choices))

    @commands.command(help="Enter a phrase/word to be γρεεκiφiεδ.")
    async def greek(self, ctx, *, arg=None):
        arg = arg or None
        if arg is None:
            await ctx.send("Please provide a word or phrase to be γρεεκiφiεδ.")
        else:
            greekMap = {
                'a': 'α',
                'b': 'β',
                'c': 'κ',
                'd': 'δ',
                'e': 'ε',
                'f': 'φ',
                'g': 'γ',
                'h': 'η',
                'j': 'ζ',
                'k': 'κ',
                'l': 'λ',
                'm': 'μ',
                'n': 'ν',
                'o': 'ο',
                'p': 'π',
                'q': 'κ',
                'r': 'ρ',
                's': 'σ',
                't': 'τ',
                'u': 'υ',
                'v': 'β',
                'w': 'ω',
                'y': 'υ',
                'x': 'ξ',
                'z': 'ζ'
            }
            newtext = []
            for i in arg:
                if i.lower() in greekMap:
                    newtext.append(greekMap[i.lower()])
                else:
                    newtext.append(i)
            greekified = ''.join(newtext)
            await ctx.send(greekified)

    @commands.command(help="Enter a phrase/word to be 丅卄工匚匚工下工乇刀.")
    async def thicc(self, ctx, *, arg=None):
        arg = arg or None
        if arg is None:
            await ctx.send("Please enter a word or phrase to be 丅卄工匚匚工下工乇刀.")
        else:
            thiccMap = {
                "a": "卂",
                "b": "乃",
                "c": "匚",
                "d": "刀",
                "e": "乇",
                "f": "下",
                "g": "厶",
                "h": "卄",
                "i": "工",
                "j": "丁",
                "k": "长",
                "l": "乚",
                "m": "从",
                "n": "\uD841\uDE28",
                "o": "口",
                "p": "尸",
                "q": "㔿",
                "r": "尺",
                "s": "丂",
                "t": "丅",
                "u": "凵",
                "v": "リ",
                "w": "山",
                "x": "乂",
                "y": "丫",
                "z": "乙"
            }
            newtext = []
            for i in arg:
                if i.lower() in thiccMap:
                    newtext.append(thiccMap[i.lower()])
                else:
                    newtext.append(i)
            thiccified = ''.join(newtext)
            await ctx.send(thiccified)

    @commands.command(
        help="Returns :regional_indicator_l: :regional_indicator_e: :regional_indicator_t: :regional_indicator_t: :regional_indicator_i: :regional_indicator_f: :regional_indicator_i: :regional_indicator_e: :regional_indicator_d: text.")
    async def letters(self, ctx, *, arg=None):
        arg = arg or None
        if arg is None:
            await ctx.send(
                "Please provide a word or phrase to be :regional_indicator_l: :regional_indicator_e: :regional_indicator_t: :regional_indicator_t: :regional_indicator_i: :regional_indicator_f: :regional_indicator_i: :regional_indicator_e: :regional_indicator_d:.")
        else:
            lettersMap = {
                "a": "🇦",
                "b": "🇧",
                "c": "🇨",
                "d": "🇩",
                "e": "🇪",
                "f": "🇫",
                "g": "🇬",
                "h": "🇭",
                "i": "🇮",
                "j": "🇯",
                "k": "🇰",
                "l": "🇱",
                "m": "🇲",
                "n": "🇳",
                "o": "🇴",
                "p": "🇵",
                "q": "🇶",
                "r": "🇷",
                "s": "🇸",
                "t": "🇹",
                "u": "🇺",
                "v": "🇻",
                "w": "🇼",
                "x": "🇽",
                "y": "🇾",
                "z": "🇿",
                "0": ":zero:",
                "1": ":one:",
                "2": ":two:",
                "3": ":three:",
                "4": ":four:",
                "5": ":five:",
                "6": ":six:",
                "7": ":seven:",
                "8": ":eight:",
                "9": ":nine:",
                "?": "❔",
                "!": "❕"
            }
            newtext = []
            for i in arg:
                if i.lower() in lettersMap:
                    newtext.append(lettersMap[i.lower()])
                else:
                    newtext.append(i)
            lettered = ' '.join(newtext)
            if len(lettered) >= 2048:
                new_letters = lettered.split(" ")
                await ctx.send("Yo your message is too long, shorten it until I fix a workaround for this")
            else:
                await ctx.send(lettered)

    @commands.command(aliases=['ct'], help="Flip a coin.")
    async def cointoss(self, ctx):
        choices = ('Heads!', 'Tails!')
        await ctx.send(random.choice(choices))

    @commands.command(help="Returns your message reversed.")
    async def reverse(self, ctx, *, message):
        message = message.split()
        await ctx.send(' '.join(reversed(message)))

    @commands.command(help="Rolls 1, 6 sided dice if given no arguments. Otherwise provide an amount of die, then how "
                           "many sides each one should have for the bot to roll that and sum the rolls.")
    async def roll(self, ctx, *choices: int):
        die_rolls = []

        def roll_die(sides, amount):
            throws = 0
            while throws < amount:
                throws += 1
                roll = random.randint(1, sides)
                yield roll

        if len(choices) == 0:
            die_amount = 1
            die_sides = 6
        else:
            die_amount = choices[0]
            die_sides = choices[1]
        if die_amount == 0 or die_sides == 0:
            await ctx.send("You need to throw at least 1 die with at least 1 side.")
        elif die_amount < 21 and die_amount != 1:
            for i in roll_die(die_sides, die_amount):
                die_rolls.append(i)
            await ctx.trigger_typing()
            await ctx.send(f"You rolled {die_amount}, {die_sides} sided die and got the following rolls: "
                           f"{''.join(str(die_rolls))}. For a total of {sum(die_rolls)}")
        else:
            for i in roll_die(die_sides, die_amount):
                die_rolls.append(i)
            await ctx.trigger_typing()
            await ctx.send(f"You rolled {die_amount}, {die_sides} sided die. For a total of {sum(die_rolls)}")

    @roll.error
    async def roll_error(self, ctx, error):
        if isinstance(error, commands.CommandInvokeError):
            await ctx.trigger_typing()
            await ctx.send("Please use a number that is more than 1 for both arguments. "
                           "Or no arguments to roll 1, 6 sided die.")
        else:
            await ctx.send(error)


class GuessGame:

    def __init__(self, bot):
        self.client = bot

    async def get_input(self, ctx, datatype, error=''):
        while True:
            try:
                message = await self.client.wait_for('message', check=lambda message: message.author is ctx.author,
                                                     timeout=60)
                message = datatype(message.content)
                return message
            except Exception:
                await ctx.send(error)

    async def gameover(self, ctx, funct):
        await ctx.send("Do you want to play again? (**Yes**/**No**)")
        self.message = await self.get_input(ctx, str)
        self.message = self.message.lower()

        if self.message == 'yes' or self.message == 'y':
            await funct()
        elif self.message == 'no' or self.message == 'n':
            await ctx.send("Thanks for playing!")
        else:
            await self.gameover(ctx, funct)

    @commands.command(help="Guess the number game.")
    async def guess(self, ctx):

        async def play():
            channel = ctx.channel
            await ctx.send("Guess a number between 1 and 100.")
            error = "Please enter a number."
            guess = await self.get_input(ctx, int, error)
            answer = random.randint(1, 100)
            counter = 0

            while guess != answer:
                counter += 1
                if guess > answer:
                    await ctx.send("{} your guess of `{}` is too high! Try again".format(ctx.author.mention, guess))
                    guess = await self.get_input(ctx, int, error)
                else:
                    await ctx.send("{} your guess of `{}` is too low! Try again".format(ctx.author.mention, guess))
                    guess = await self.get_input(ctx, int, error)
            else:
                if counter <= 1:
                    await ctx.send("Congratulations! You got it on the first attempt!")
                else:
                    await ctx.send(f"Congratulations! It took you {counter} tries to guess the correct number.")
                await self.gameover(ctx, play)

        await play()

    @commands.command(help="Rock paper scissors game.")
    async def rps(self, ctx):
        async def play():
            await ctx.send("Let's play rock, paper, scissors. Select your weapon:")
            choices = ('rock', 'paper', 'scissors')
            computer = choices[random.randint(0, 2)]
            player = await self.get_input(ctx, str)
            player = player.lower()
            if player == 'r':
                player = 'rock'
            elif player == 's':
                player = 'scissors'
            elif player == 'p':
                player = 'paper'
            else:
                player = player

            beats = {'rock': ['paper'],
                     'paper': ['scissors'],
                     'scissors': ['rock']}

            if computer and player in choices:
                if computer == player:
                    await ctx.send(f"**Tie!** You both chose {computer.title()}.")
                    await self.gameover(ctx, play)
                elif player in beats[computer]:
                    await ctx.send(f"**You win!** Moosebot chose: {computer.title()}, and you chose: {player.title()}.")
                    await self.gameover(ctx, play)
                else:
                    await ctx.send(
                        f"**You lose!** Moosebot chose: {computer.title()}, and you chose: {player.title()}.")
                    await self.gameover(ctx, play)
            else:
                await play()

        await play()


class Counting:

    def __init__(self, bot):
        self.client = bot

    @commands.command()
    @commands.check(is_owner)
    async def count(self, ctx):
        if ctx.channel.topic and ctx.channel.topic.startswith(">count"):
            return None
        else:
            await ctx.channel.edit(topic=">count | The next message must start with 1")

    async def on_message(self, ctx):
        if ctx.guild is None:
            return None
        elif ctx.author == client.user:
            return None
        else:
            if ctx.content.startswith(">count"):
                pass
            elif ctx.channel.topic and ctx.channel.topic.startswith(">count"):
                count = int(ctx.channel.topic.split()[8])
                if count is None:
                    return None
                elif ctx.content.startswith(f"{count} ") or ctx.content == str(count):
                    await ctx.channel.edit(topic=f">count | The next message must start with {count+ 1}")
                else:
                    await ctx.channel.purge(limit=1)
                    await ctx.channel.send(
                        f"{ctx.author.mention} The next message in this channel must start with {count}!",
                        delete_after=2.0)


@client.command()
async def simage(ctx):
    await ctx.send(ctx.guild.icon_url)


async def saveattach(message):
    if message.author.id == 445936072288108544:
        return None
    else:
        channel = message.guild.get_channel(449821022846320641)
        if len(message.attachments) >= 1:
            path = "database/attachments/"
            for i in message.attachments:
                url = i.url
                data = get_image(url)
                file_name = str(i.id)
                file_type = i.url[-4:]
                types = [".png", ".mp4", ".jpg", ".gif", ".gifv", ".mp3", ".jpeg", ".mov"]
                if file_type in types:
                    save_image(path, file_name, data, file_type)
                else:
                    file_type = i.url[-5:]
                    if file_type in types:
                        save_image(path, file_name, data, file_type)
                    else:
                        file_type = ".png"
                        save_image(path, file_name, data, file_type)
                file_type = i.url[-4:]
                file_path = os.path.join(path, file_name + file_type)
                await asyncio.sleep(2)
                if message.guild.id == 427010987334434816:
                    await channel.send(file=discord.File(file_path))


async def rad(message):
    dard = client.get_emoji(446703695204450305)
    if message.content == "<:rad:428937672552349698>":
        await message.add_reaction(dard)


async def dar(message):
    radical = client.get_emoji(428937672552349698)
    if message.content == "<:dar:446703695204450305>":
        await message.add_reaction(radical)


@client.command(help="Enter an amount of messages to purge from the chat.")
@commands.check(is_mod)
async def clear(ctx, amount: int= None):
    amount = amount or None
    if amount is None:
        amount = 1
    deleted = await ctx.channel.purge(limit=amount + 1)
    await ctx.send(f"I have cleared `{len(deleted)- 1}` messages.", delete_after=0.5)


@client.command()
@commands.check(is_owner)
async def hangup(ctx):
    if len(phone_channel_list) == 2:
        for i in phone_channel_list:
            await i.send("Owner forcibly hung up the phone to use it himself lmoa")
            await ctx.message.delete()
        del phone_channel_list[:]
    else:
        await ctx.send("You idiot, the phone isn't being used rn")
        await ctx.message.delete()


@client.command(help="Calls another server on the phone.")
async def phone(ctx):
    channel = ctx.channel
    this_server = ctx.guild
    if len(phone_channel_list) == 0:
        phone_server_list.append(this_server)
        phone_channel_list.append(channel)
        await ctx.send("Calling on the phone")
        await ctx.message.delete()
    elif channel not in phone_channel_list and len(phone_channel_list) == 2:
        await ctx.message.delete()
        await ctx.send("The phone is currently in use. Please wait and try again later")
    elif channel == phone_channel_list[0]:
        await ctx.send("Hanging up the phone")
        await phone_channel_list[1].send("The other party hung up the phone, "
                                         "use the command again to start another call!")
        await ctx.message.delete()
        del phone_channel_list[:]
    elif channel in phone_channel_list:
        await ctx.send("Hanging up the phone")
        await phone_channel_list[0].send("The other party hung up the phone, "
                                         "use the command again to start another call!")
        await ctx.message.delete()
        del phone_channel_list[:]
    elif channel not in phone_channel_list and len(phone_channel_list) == 1:
        phone_channel_list.append(channel)
        phone_server_list.append(this_server)
        await phone_channel_list[0].send("You are now connected to someone through the phone, say hi!")
        await phone_channel_list[1].send("You are now connected to someone through the phone, say hi!")


async def mobile(ctx):
    channel = ctx.channel
    if ctx.message.author.bot:
        return None
    elif ctx.message.content == ">phone":
        return None
    elif len(ctx.message.embeds) > 0:
        return None
    elif len(ctx.message.attachments) > 0:
        return None
    elif len(phone_channel_list) == 2:
        if channel == phone_channel_list[0]:
            await phone_channel_list[1].send("**{}**#{}: {}".format(ctx.message.author.name,
                                                                    ctx.message.author.discriminator,
                                                                    ctx.message.content))
        elif channel == phone_channel_list[1]:
            await phone_channel_list[0].send("**{}**#{}: {}".format(ctx.message.author.name,
                                                                    ctx.message.author.discriminator,
                                                                    ctx.message.content))


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


class FullMember(commands.Converter):
    async def convert(self, ctx, argument):
        try:
            arg = await commands.MemberConverter().convert(ctx, argument)
            return arg
        except commands.BadArgument:
            arg = [i for i in ctx.guild.members if
                   i.name.lower() == argument.lower() or i.display_name.lower() == argument.lower()]
            if len(arg) >= 1:
                return arg[0]
            else:
                arg = [i for i in ctx.guild.members if
                       i.name.lower().startswith(argument.lower()) or i.display_name.lower().startswith(
                           argument.lower())]
                if len(arg) >= 1:
                    return arg[0]
                else:
                    return argument


class PartialMember(commands.Converter):
    async def convert(self, ctx, argument):
        if len(argument) == 1 and not isinstance(argument, discord.Member):
            return argument
        else:
            try:
                arg = await commands.MemberConverter().convert(ctx, argument)
                return arg
            except commands.BadArgument:
                arg = [i for i in ctx.guild.members if
                       i.name.lower() == argument.lower() or i.display_name.lower() == argument.lower()]
                if len(arg) >= 1:
                    return arg[0]
                else:
                    arg = [i for i in ctx.guild.members if
                           i.name.lower().startswith(argument.lower()) or i.display_name.lower().startswith(
                               argument.lower())]
                    if len(arg) >= 1:
                        return arg[0]
                    else:
                        return argument


@client.command(help="Get's a users avatar.")
async def avatar(ctx, *, member: FullMember = None):
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


class RolesConverter(commands.Converter):
    async def convert(self, ctx, arg):
        try:
            arg = await commands.RoleConverter().convert(ctx, arg)
            return arg
        except commands.BadArgument:
            arg = arg.lower()
            role = [x for x in ctx.guild.roles if x.name.lower() == arg or x.name.lower().startswith(arg)]
            if len(role) == 0:
                await ctx.send(f"There is no role `{arg}`.")
            else:
                return role[0]


class Info:

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def roles(self, ctx, user: FullMember= None):
        user = user or ctx.author
        roles = '\n'.join([x.name for x in user.roles][1:])
        embed = discord.Embed(title=f"{user.display_name}'s roles.", description=roles, colour=0xb18dff)
        embed.set_thumbnail(url=user.avatar_url)

        await ctx.send(embed=embed)

    @commands.command(aliases=["fb"], description="Send feedback to the bot author.")
    async def feedback(self, ctx, *, arg):
        user = client.get_user(192519529417408512)
        embed = discord.Embed(
            title=f"Feedback from {ctx.author.name}({ctx.author.id}) on {ctx.guild.name}({ctx.guild.id}):",
            description=arg, colour=0xb18dff)
        await user.send(embed=embed)
        await ctx.send("Feedback sent! Thank you!")

    @commands.command(help="Give a role name to get a list of users in that role.")
    async def inrole(self, ctx, *, role: RolesConverter):
        users = [x.display_name for x in role.members]
        embed = discord.Embed(
            title=f"{len(role.members)} {'users' if len(role.members) != 1 else 'user'} in {role.name}",
            description=f"`{'`, `'.join(users)}`",
            colour=0xb18dff if role.colour == discord.Colour(000000) else role.colour)
        await ctx.send(embed=embed)

    @inrole.error
    async def inrole_error(self, ctx, error):
        await ctx.send(error)

    @commands.command(aliases=['user', 'ui'], help="Provides information about a user.")
    async def userinfo(self, ctx, *, member: FullMember= None):
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


class Experience:

    def __init__(self, bot):
        self.bot = bot
        self.xpPath = 'database/experience/experience_'
        self.lvlPath = 'database/experience/levels_'

    def save(self, list, path):
        with open(path, 'w') as write_file:
            json.dump(list, write_file, indent=4)

    def load(self, path):
        firstline = dict()
        if os.path.exists(path):
            with open(path, 'r') as read_file:
                data = json.load(read_file)
            return data
        else:
            s = json.dumps(firstline)
            with open(path, 'w+') as new_file:
                new_file.write(s)
                data = json.load(new_file)
            return data

    async def on_message(self, message):
        if message.guild is None:
            return
        else:
            if message.author.bot:
                return
            else:
                await asyncio.gather(self.grantxp(message))

    @commands.command(aliases=['lb'], help='See who has a life the least on your server.')
    async def leaderboard(self, ctx):
        xp_list = sorted(self.load(self.xpPath + f'{ctx.guild.id}.json').items(), key=lambda kv: kv[1], reverse=True)
        level_list = sorted(self.load(self.lvlPath + f'{ctx.guild.id}.json').items(), key=lambda kv: kv[1], reverse=True)
        order = 1
        format = ""
        for i in level_list:
            user = i[0]
            try:
                client.get_user(int(i[0]))
                format += f'▫{order}. **{client.get_user(int(i[0])).display_name}**: {str(i[1])} `({[str(x[1]) for x in xp_list if x[0] == user][0]} exp)` \n'
                order += 1
            except AttributeError:
                # format += f'▫{order}. **<@{i[0]}>**: {str(i[1])} `({[str(x[1]) for x in xp_list if x[0] == user][0]} exp)` \n'
                order -= 1


        embed = discord.Embed(title="Experience leaderboard", description=format, colour=0xb18dff)
        await ctx.send(embed=embed)

    @commands.command(aliases=['lvl', 'rank'], help='Check your current xp and level standings.')
    async def level(self, ctx):
        xp_list = self.load(self.xpPath + f'{ctx.guild.id}.json')
        level_list = sorted(self.load(self.lvlPath + f'{ctx.guild.id}.json').items(), key=lambda kv: kv[1], reverse=True)
        for i in level_list:
            if int(i[0]) == ctx.author.id:
                user = i
        embed = discord.Embed(title=f"{ctx.author.display_name}'s level details",
                              description=f"**Rank:** {level_list.index(user) + 1} \n**Level:** {user[1]}\n**Experience:** {str(xp_list[str(ctx.author.id)])}", colour=0xb18dff)
        await ctx.send(embed=embed)

    @commands.command(aliases=['gvxp'], help='Bot author only command.')
    @commands.check(is_owner)
    async def givexp(self, ctx, user: FullMember= None, *, args: int):
        xp_list = self.load(self.xpPath + f'{ctx.guild.id}.json')
        user = user or None
        args = args or None
        if user is None:
            await ctx.send("Please tell me who to give xp to.")
        elif args is None:
            await ctx.send(f"Please tell me how much xp to give to `{user.display_name}`.")
        else:
            xp_list[str(user.id)] += args
            self.save(xp_list, self.xpPath + f'{ctx.guild.id}.json')
            await ctx.send(f"{args} xp successfully given to {user.display_name}.")

    @commands.command(aliases=['rmvxp'], help='Bot author only command.')
    @commands.check(is_owner)
    async def removexp(self, ctx, user: FullMember = None, *, args):
        xp_list = self.load(self.xpPath + f'{ctx.guild.id}.json')
        user = user or None
        args = args or None
        if user is None:
            await ctx.send("Please tell me who to take xp from.")
        elif args is None:
            await ctx.send(f"Please tell me how much xp to take from `{user.display_name}`.")
        else:
            if args == 'all' or args == '*':
                beforexp = xp_list[str(user.id)]
                xp_list[str(user.id)] = 0
                await ctx.send(f"{beforexp} xp successfully taken from {user.display_name}.")
            else:
                xp_list[str(user.id)] -= int(args)
                await ctx.send(f"{args} xp successfully taken from {user.display_name}.")
            self.save(xp_list, self.xpPath + f'{ctx.guild.id}.json')

    async def grantxp(self, message):
        author = str(message.author.id)
        xp_list = self.load(self.xpPath + f'{message.guild.id}.json')
        level_list = self.load(self.lvlPath + f'{message.guild.id}.json')

        if author in xp_list:
            xp_list[author] += random.randint(1, 10)
            self.save(xp_list, self.xpPath + f'{message.guild.id}.json')
        else:
            xp_list[author] = random.randint(1, 10)
            self.save(xp_list, self.xpPath + f'{message.guild.id}.json')
        if author in level_list:
            level_amount = 100
            newlevel = 0
            userxp = xp_list[author]
            levelxp = 0
            while levelxp < userxp:
                levelxp += int(level_amount)
                level_amount = (level_amount * 0.04) + level_amount
                newlevel += 1
                if levelxp > xp_list[author]:
                    newlevel -= 1
            if newlevel != level_list[author]:
                await message.channel.send(f"Congratulations {message.author.mention} you leveled up to level {newlevel}!")
                level_list[author] = newlevel
                self.save(level_list, self.lvlPath + f'{message.guild.id}.json')
        else:
            level_list[author] = int(xp_list[author] / 100)
            self.save(level_list, self.lvlPath + f'{message.guild.id}.json')


class Economy:

    def __init__(self, bot):
        self.bot = bot
        self.moneypath = "database/economy/money.json"

    def save(self, list, path):
        with open(path, 'w') as write_file:
            json.dump(list, write_file, indent=4)

    def load(self, path):
        firstline = dict()
        if os.path.exists(path):
            with open(path, 'r') as read_file:
                data = json.load(read_file)
            return data
        else:
            s = json.dumps(firstline)
            with open(path, 'w+') as new_file:
                new_file.write(s)
                data = json.load(new_file)
            return data

    async def on_message(self, message):
        if message.guild is None:
            return
        elif message.author.bot:
            return
        else:
            await asyncio.gather(self.pickchance(message))

    async def pickchance(self, message):
        chance = random.randint(1, 1000)
        amount = random.randint(1, 200)
        money_list = self.load(self.moneypath)
        if chance < 20:
            gen_message = await message.channel.send(f"`{amount}Ᵽ` has spawned! Type `dab` to collect it! You have 60 seconds")

            def check(m):
                return m.content.lower() == 'dab' and m.channel == message.channel
            try:
                msg = await client.wait_for('message', check=check, timeout=60)
                if str(msg.author.id) in money_list:
                    money_list[str(msg.author.id)] += amount
                    await message.channel.send(
                        f"{msg.author.mention} dabbed on the Ᵽlaceholders. `{amount}Ᵽ` awarded to them.")
                    await gen_message.edit(
                        content=f"~~`{amount}Ᵽ` has spawned! Type `dab` to collect it! You have 60 seconds~~")
                else:
                    money_list[str(msg.author.id)] = amount
                    await message.channel.send(
                        f"{msg.author.mention} dabbed on the Ᵽlaceholders. `{amount}Ᵽ` awarded to them.")
                    await gen_message.edit(
                        content=f"~~`{amount}Ᵽ` has spawned! Type `dab` to collect it! You have 60 seconds~~")
                self.save(money_list, self.moneypath)

            except asyncio.TimeoutError:
                await message.channel.send("You took to long to dab the Ᵽ.")
                await gen_message.edit(
                    content=f"~~`{amount}Ᵽ` has spawned! Type `dab` to collect it! You have 60 seconds~~")

    @commands.command(aliases=['bal'], help='Check your balance.')
    async def balance(self, ctx):
        money_list = self.load(self.moneypath)

        if str(ctx.author.id) in money_list:
            if money_list[str(ctx.author.id)] == 0:
                usermoney = 'You literally are broke af. 0 Ᵽlaceholders.'
            else:
                usermoney = f'{str(money_list[str(ctx.author.id)])}Ᵽ'
        else:
            usermoney = 'You literally are broke af. 0 Ᵽlaceholders.'
        embed = discord.Embed(title=f"{ctx.author.display_name}'s Ᵽlaceholders.", description=usermoney, colour=0xb18dff)
        await ctx.send(embed=embed)

    @commands.command(help='Generate Ᵽlaceholders for a user from thin air. (Admin only)')
    @commands.check(is_owner)
    async def givep(self, ctx, amount: int, *, user: FullMember):
        money_list = self.load(self.moneypath)
        user = user or None
        amount = amount or None
        if user is None or not isinstance(user, discord.Member):
            await ctx.send("Please tell me who to give the Ᵽlaceholders to.")
        elif amount is None:
            await ctx.send("Please tell me how many Ᵽlaceholders to give.")
        else:
            try:
                int(amount)
                if str(user.id) in money_list:
                    money_list[str(user.id)] += amount
                else:
                    money_list[str(user.id)] = amount
                self.save(money_list, self.moneypath)
                await ctx.send(f'`{amount}Ᵽ` was given to `{user.display_name}`')
            except Exception:
                await ctx.send("The amount to give the person needs to be a number.")

    @commands.command(help='Take Ᵽlaceholders from someone and delete them to the abyss. (Admin only)')
    @commands.check(is_owner)
    async def takep(self, ctx, amount=None, *, user: FullMember=None):
        money_list = self.load(self.moneypath)
        user = user or None
        amount = amount or None
        if user is None or not isinstance(user, discord.Member):
            await ctx.send("Please tell me who to take the Ᵽlaceholders from.")
        elif amount is None:
            await ctx.send("Please tell me how many Ᵽlaceholders to take.")
        else:
            try:
                amount = int(amount)
                if str(user.id) in money_list:
                    if money_list[str(user.id)] == 0:
                        await ctx.send(f"`{user.display_name} is already poor enough, no more can be taken from them.")
                    elif money_list[str(user.id)] - amount < 0:
                        await ctx.send(f"Doing this would cause `{user.display_name}` to go in to debt. Instead, we just set them to 0Ᵽ.")
                        money_list[str(user.id)] = 0
                        await ctx.send(f'`{user.display_name}` is now poor.')
                    else:
                        money_list[str(user.id)] -= amount
                        await ctx.send(f'`{amount}Ᵽ` was taken from `{user.display_name}`')
                else:
                    await ctx.send(f'{user.display_name} literally has no Ᵽlaceholders to take.')
                    money_list[str(user.id)] = 0
                self.save(money_list, self.moneypath)

            except ValueError:
                await ctx.send("It needs to be `>takep amount user`")

    @commands.command(help='Pay another user some Ᵽlaceholders.')
    async def pay(self, ctx, amount=None, *, user: FullMember=None):
        user = user or None
        amount = amount or None
        money_list = self.load(self.moneypath)
        if user is None or not isinstance(user, discord.Member):
            await ctx.send("Use the command like this `>pay amount user`")
        elif amount is None:
            await ctx.send("Use the command like this `>pay amount user`")
        else:
            try:
                amount = int(amount)
                if not str(ctx.author.id) in money_list:
                    await ctx.send("You do not have enough Ᵽlaceholders to give that amount.")
                    money_list[str(ctx.author.id)] = 0
                elif amount <= 0:
                    await ctx.send("You need to give an amount more than 0.")
                elif amount > money_list[str(ctx.author.id)]:
                    await ctx.send("You do not have enough Ᵽlaceholders to give that amount.")
                else:
                    money_list[str(ctx.author.id)] -= amount
                    if not str(user.id) in money_list:
                        money_list[str(user.id)] = amount
                    else:
                        money_list[str(user.id)] += amount
                    self.save(money_list, self.moneypath)
                    await ctx.send(f"You have paid `{user.display_name}` {amount}Ᵽ")

            except ValueError:
                await ctx.send("The amount to pay needs to be a number.")

    @commands.command(help='Attempt to steal Ᵽlaceholders from other Members. Be careful though, a failure will result in them stealing from you! Chances are low.')
    #@commands.cooldown(1, 3600, commands.BucketType.user)
    async def steal(self, ctx, amount=None, *, user: FullMember=None):
        amount = amount or None
        user = user or None
        money_list = self.load(self.moneypath)
        if user is None or not isinstance(user, discord.Member):
            await ctx.send("Use the command like this `>steal amount user`")
        elif amount is None:
            await ctx.send("Use the command like this `>steal amount user`")
        else:
            try:
                amount = int(amount)
                if str(ctx.author.id) not in money_list:
                    money_list[str(ctx.author.id)] = 0
                if amount <= 0:
                    await ctx.send("You need to try to steal at least something...")
                elif str(user.id) not in money_list:
                    await ctx.send("That user does not have enough Ᵽlaceholders to steal that amount.")
                    money_list[str(user.id)] = 0
                elif money_list[str(user.id)] < amount:
                    await ctx.send("That user does not have enough Ᵽlaceholders to steal that amount.")
                    money_list[str(user.id)] = 0
                else:
                    chance = random.randint(1, 10000)
                    if amount >= (money_list[str(user.id)] * 0.95):
                        if chance == 666:
                            await ctx.send(f"You succeeded! Wow. What are the chances of that. {user.display_name} must have no sense of awareness.")
                            money_list[str(ctx.author.id)] += amount
                            money_list[str(user.id)] -= amount
                        else:
                            lose = int((money_list[str(ctx.author.id)] * 0.7))
                            if money_list[str(ctx.author.id)] == 0:
                                await ctx.send(f"You failed. {user.display_name} noticed you and beat you to a pulp. However you are dirt poor, so instead they took an item from you.(implemented soon)")
                            else:
                                await ctx.send(f"You failed. {user.display_name} noticed and beat you to a pulp, taking what you had on you with them. You lost {lose}Ᵽ.")
                                money_list[str(ctx.author.id)] -= lose
                                money_list[str(user.id)] += lose
                    elif amount >= int((money_list[str(user.id)] * 0.9)):
                        if chance in [6, 9]:
                            await ctx.send(f"You snuck into {user.display_name}'s pockets and grabbed out {amount}. Luckily they didn't notice. This payed off big time.")
                            money_list[str(ctx.author.id)] += amount
                            money_list[str(user.id)] -= amount
                        else:
                            lose = int((money_list[str(ctx.author.id)] * 0.6))
                            if money_list[str(ctx.author.id)] == 0:
                                await ctx.send(f"You failed. {user.display_name} noticed you and beat you to a pulp. However you are dirt poor, so instead they took an item from you.(implemented soon)")
                            else:
                                await ctx.send(f"You failed. {user.display_name} noticed and beat you to a pulp, taking what you had on you with them. You lost {lose}Ᵽ.")
                                money_list[str(ctx.author.id)] -= lose
                                money_list[str(user.id)] += lose
                    elif amount >= int((money_list[str(user.id)] * 0.8)):
                        if 8000 >= chance <= 8050:
                            await ctx.send(f"You snuck into {user.display_name}'s pockets and grabbed out {amount}Ᵽ. Luckily they didn't notice. That was well worth it.")
                            money_list[str(ctx.author.id)] += amount
                            money_list[str(user.id)] -= amount
                        else:
                            lose = int((money_list[str(ctx.author.id)] * 0.5))
                            if money_list[str(ctx.author.id)] == 0:
                                await ctx.send(f"You failed. {user.display_name} noticed you and beat you to a pulp. However you are dirt poor, so instead they took an item from you.(implemented soon)")
                            else:
                                await ctx.send(f"You failed. {user.display_name} noticed and beat you to a pulp, taking what you had on you with them. You lost {lose}Ᵽ.")
                                money_list[str(ctx.author.id)] -= lose
                                money_list[str(user.id)] += lose
                    elif amount >= int((money_list[str(user.id)] * 0.7)):
                        if 4500 >= chance <= 4600:
                            await ctx.send(f"You snuck into {user.display_name}'s pockets and grabbed out {amount}Ᵽ. Luckily they didn't notice. Risky.")
                            money_list[str(ctx.author.id)] += amount
                            money_list[str(user.id)] -= amount
                        else:
                            lose = int((money_list[str(ctx.author.id)] * 0.45))
                            if money_list[str(ctx.author.id)] == 0:
                                await ctx.send(f"You failed. {user.display_name} noticed you and beat you to a pulp. However you are dirt poor, so instead they took an item from you.(implemented soon)")
                            else:
                                await ctx.send(f"You failed. {user.display_name} noticed and beat you to a pulp, taking what you had on you with them. You lost {lose}Ᵽ.")
                                money_list[str(ctx.author.id)] -= lose
                                money_list[str(user.id)] += lose
                    elif amount >= int((money_list[str(user.id)] * 0.6)):
                        if 1001 >= chance <= 1450:
                            await ctx.send(f"You snuck into {user.display_name}'s pockets and grabbed out {amount}Ᵽ. Luckily they didn't notice.")
                            money_list[str(ctx.author.id)] += amount
                            money_list[str(user.id)] -= amount
                        else:
                            lose = int((money_list[str(ctx.author.id)] * 0.25))
                            if money_list[str(ctx.author.id)] == 0:
                                await ctx.send(f"You failed. {user.display_name} noticed you and beat you to a pulp. However you are dirt poor, so instead they took an item from you.(implemented soon)")
                            else:
                                await ctx.send(f"You failed. {user.display_name} noticed and beat you to a pulp, taking what you had on you with them. You lost {lose}Ᵽ.")
                                money_list[str(ctx.author.id)] -= lose
                                money_list[str(user.id)] += lose
                    elif amount >= int((money_list[str(user.id)] * 0.5)):
                        if 250 >= chance <= 1000:
                            await ctx.send(f"You snuck into {user.display_name}'s pockets and grabbed out {amount}Ᵽ. Luckily they didn't notice.")
                            money_list[str(ctx.author.id)] += amount
                            money_list[str(user.id)] -= amount
                        else:
                            lose = int((money_list[str(ctx.author.id)] * 0.2))
                            if money_list[str(ctx.author.id)] == 0:
                                await ctx.send(f"You failed. {user.display_name} noticed you and beat you to a pulp. However you are dirt poor, so instead they took an item from you.(implemented soon)")
                            else:
                                await ctx.send(f"You failed. {user.display_name} noticed and beat you to a pulp, taking what you had on you with them. You lost {lose}Ᵽ.")
                                money_list[str(ctx.author.id)] -= lose
                                money_list[str(user.id)] += lose
                    else:
                        await ctx.send("You're a real penny pincher huh? Go earn money some other way. You're not gonna nickel and dime your way to the top.")
                        ctx.command.reset_cooldown()
                    self.save(money_list, self.moneypath)
            except ValueError:
                await ctx.send("You need to give a number to steal.")

    # @steal.error
    # async def steal_error(self, ctx, error):
    #     if isinstance(error, commands.errors.CommandOnCooldown):
    #         await ctx.send(f"You recently tried to steal. You need to wait {int(error.retry_after / 60)} minutes to try again.")
    #     else:
    #         print(error)

    @commands.command(help='Get Ᵽlaceholders on the daily')
    @commands.cooldown(1, 86400, commands.BucketType.user)
    async def daily(self, ctx):
        money_list = self.load(self.moneypath)
        if str(ctx.author.id) in money_list:
            money_list[str(ctx.author.id)] += 500
        else:
            money_list[str(ctx.author.id)] = 500
        await ctx.send("500Ᵽ awarded for daily!")
        self.save(money_list, self.moneypath)

    @daily.error
    async def daily_error(self, ctx, error):
        if isinstance(error, commands.errors.CommandOnCooldown):
            await ctx.send(f"You can only use this command once per day. Try again in {int(error.retry_after / 60 / 60 + 1)} hours.")
        else:
            print(error)

    @commands.command(aliases=['baltop', 'richlist', 'ballb'], help='See the list of the richest people.')
    async def balancelb(self, ctx):
        money_list = sorted(self.load(self.moneypath).items(), key=lambda kv: kv[1], reverse=True)
        order = 1
        eligable = []
        for i in money_list:
            try:
                client.get_user(int(i[0]))
                if i[1] == 0:
                    continue
                else:
                    eligable.append(f'▫{order}. **{client.get_user(int(i[0])).display_name}**: {i[1]}Ᵽ\n')
                    order += 1
            except AttributeError:
                continue

        pagesamount = int(len(eligable) / 10)
        leftover = len(eligable) % 10
        page = 0
        pages = []
        amount1 = 0
        amount2 = 10
        while page < pagesamount:
            pages.append(eligable[amount1:amount2])
            amount1 += 10
            amount2 += 10
            page += 1
        pages.append(eligable[-leftover:])
        curpage = 0
        foot_page = 1
        embed = discord.Embed(title="Balance Leaderboard.", description=''.join(pages[curpage]), colour=0xb18dff)
        embed.set_footer(text=f'Page ({foot_page}/{pagesamount+1})')
        msg = await ctx.send(embed=embed)
        await msg.add_reaction('◀')
        await msg.add_reaction('▶')

        def check(reaction, user):
            return str(reaction.emoji) == '◀' or str(reaction.emoji) == '▶' and user == ctx.author
        while True:
            try:
                reaction, user = await client.wait_for('reaction_add', timeout=10, check=check)
            except asyncio.TimeoutError:
                await msg.clear_reactions()
                return
            else:
                if str(reaction.emoji) == '◀' and user == ctx.author:
                    if curpage == 0:
                        await msg.remove_reaction(emoji='◀', member=ctx.author)
                        continue
                    else:
                        foot_page -= 1
                        embed = discord.Embed(title="Balance Leaderboard.", description=''.join(pages[curpage-1]), colour=0xb18dff)
                        embed.set_footer(text=f'Page ({foot_page}/{pagesamount+1})')
                        await msg.edit(embed=embed)
                        curpage -= 1
                    await msg.remove_reaction(emoji='◀', member=ctx.author)
                elif str(reaction.emoji) == '▶' and user == ctx.author:
                    if curpage == pagesamount:
                        await msg.remove_reaction(emoji='▶', member=ctx.author)
                        continue
                    else:
                        foot_page += 1
                        embed = discord.Embed(title="Balance Leaderboard.", description=''.join(pages[curpage+1]), colour=0xb18dff)
                        embed.set_footer(text=f'Page ({foot_page}/{pagesamount+1})')
                        await msg.edit(embed=embed)
                        curpage += 1
                    await msg.remove_reaction(emoji='▶', member=ctx.author)

    @commands.command(aliases=['cf', 'bf', 'betflip'], help='Flip a coin and bet heads or tails. Win to double up.')
    async def coinflip(self, ctx,  amount=None, side=None):
        money_list = self.load(self.moneypath)
        side = side or None
        amount = amount or 1
        sides = ['t', 'h', 'tail', 'head']
        choices = ['heads', 'tails']
        if money_list[str(ctx.author.id)] <= 0:
            await ctx.send(
                "You are broke. You cannot bet. Earn some Ᵽlaceholders... Or steal them...")
            return
        if side is None or side.lower() not in sides:
            await ctx.send('Please tell me what side you want to bet on. (h/t)')

            def check(m):
                return m.author == ctx.author and m.content.lower() == 'h' or m.content.lower() == 't'
            try:
                msg = await client.wait_for('message', check=check, timeout=15)
                side = 'heads' if msg.content.lower() == 'h' else 'tails'
                await ctx.send(f"Please tell me how much Ᵽ you want to bet on {side}.")

                def check(m):
                    return m.author == ctx.author
                try:
                    msg = await client.wait_for('message', check=check, timeout=15)
                    if msg.content.lower() == 'all':
                        amount = money_list[str(ctx.author.id)]
                    else:
                        try:
                            amount = int(msg.content)
                        except Exception:
                            await ctx.send("You need to give me a number to gamble. Not whatever that was...")
                            return
                    if str(ctx.author.id) in money_list:
                        flipside = random.choice(choices)
                        if flipside == side.lower():
                            await ctx.send(f"I flipped {flipside.title()}, you win `{amount}Ᵽ`")
                            money_list[str(ctx.author.id)] += int(amount)
                        else:
                            await ctx.send(f"I flipped {flipside.title()}, you lose. Sorry.")
                            money_list[str(ctx.author.id)] -= int(amount)
                        self.save(money_list, self.moneypath)
                    else:
                        await ctx.send("You are broke. You cannot bet. Earn some Ᵽlaceholders... Or steal them...")

                except asyncio.TimeoutError:
                    await ctx.send("You took too long to reply.")
            except asyncio.TimeoutError:
                await ctx.send("You took too long to reply.")
        else:
            if side.lower() == 'h':
                side = 'heads'
            elif side.lower() == 't':
                side = 'tails'
            try:
                amount = int(amount)
                if str(ctx.author.id) in money_list:
                    if money_list[str(ctx.author.id)] <= 0:
                        await ctx.send("You are broke. You cannot bet. Earn some Ᵽlaceholders... Or steal them...")
                    else:
                        flipside = random.choice(choices)
                        if flipside == side.lower():
                            await ctx.send(f"I flipped {flipside.title()}, you win `{amount}Ᵽ`")
                            money_list[str(ctx.author.id)] += int(amount)
                        else:
                            await ctx.send(f"I flipped {flipside.title()}, you lose. Sorry.")
                            money_list[str(ctx.author.id)] -= int(amount)
                        self.save(money_list, self.moneypath)
                else:
                    await ctx.send("You are broke. You cannot bet. Earn some Ᵽlaceholders... Or steal them...")
            except Exception:
                if amount.lower() == 'all':
                    amount = money_list[str(ctx.author.id)]
                    flipside = random.choice(choices)
                    if flipside == side.lower():
                        await ctx.send(f"I flipped {flipside.title()}, you win `{amount}Ᵽ`")
                        money_list[str(ctx.author.id)] += int(amount)
                    else:
                        await ctx.send(f"I flipped {flipside.title()}, you lose. Sorry.")
                        money_list[str(ctx.author.id)] -= int(amount)
                    self.save(money_list, self.moneypath)
                else:
                    await ctx.send("You need to give me a number to gamble. Not whatever that was...")

    # @commands.command(aliases=['bj'])
    # async def blackjack(self, ctx, amount= None):
    #     money_list = self.load(self.moneypath)
    #     usermoney = money_list[str(ctx.author.id)]
    #     amount = amount or None
    #     if amount is None:
    #         await ctx.send("Use the command like this `>bj amount`.")
    #     try:
    #         amount = int(amount)
    #     except ValueError:
    #         await ctx.send("You must enter a value to bet. Not whatever that was...")
    #
    #     if amount > usermoney:
    #         await ctx.send("You do not have that much to bet.")
    #     elif amount <= 0:
    #         await ctx.send("You need to at least bet something.")
    #     elif amount == 'all' or amount == '*':
    #         amount = usermoney
    #     embed = discord.Embed(title=f'Blackjack with {ctx.author.display_name} ({amount}Ᵽ)',
    #                           description="Get the total value of your cards as close to 21 without going over (bust). "
    #                                       "\nIf you win, you double up. If we draw, you get your money back.\nType `hit` to draw another card. \nType `stand` to stick with what you've got.")
    #     cards_clubs = ['A', 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 'J', 'Q', 'K']
    #     cards_spades = ['A', 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 'J', 'Q', 'K']
    #     cards_diamonds = ['A', 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 'J', 'Q', 'K']
    #     cards_hearts = ['A', 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 'J', 'Q', 'K']
    #     faces = ['J', 'Q', 'K']
    #     dealer_hand = []
    #     dealer_suits = []
    #     player_hand = []
    #     player_suits = []
    #
    #     def deal(hand, suits):
    #         dealt = 0
    #         while dealt < 2:
    #             deck = random.choice([cards_clubs, cards_spades, cards_hearts, cards_diamonds])
    #             card = random.choice(deck)
    #             hand.append(card)
    #             if deck == cards_diamonds:
    #                 suits.append('♦')
    #             elif deck == cards_hearts:
    #                 suits.append('♥')
    #             elif deck == cards_spades:
    #                 suits.append('♠')
    #             else:
    #                 suits.append('♣')
    #             deck.remove(card)
    #             dealt += 1
    #
    #     deal(dealer_hand, dealer_suits)
    #     deal(player_hand, player_suits)
    #     print(dealer_hand)
    #     print(player_hand)
    #
    #     def check_win(hand):
    #         if 'A' in hand:
    #             hand.remove('A')
    #             if sum(hand) + 11 == 21:
    #                 return True
    #             elif sum(hand) + 1 == 21:
    #                 return False
    #         else:
    #             if sum(hand) > 21:
    #                 return False
    #             elif sum(hand) == 21:
    #                 return True
    #
    #     def check_hand(hand):
    #         if hand[0] == 'A':
    #             if hand[1] + 11 == 21:
    #                 return True
    #             else:
    #                 return False
    #         elif hand[1] == 'A':
    #             if hand[0] + 11 == 21:
    #                 return True
    #             else:
    #                 return False
    #         else:
    #             return False
    #
    #     def check_card(hand):
    #         if hand[0] in faces:
    #             return '10'
    #         elif hand[0] == 'A':
    #             return '1/11'
    #         else:
    #             return hand[0]
    #
    #     if check_hand(dealer_hand):
    #         embed.add_field(name="Moosebot's Hand (21)", value=f'{dealer_hand[0]}{dealer_suits[0]}{dealer_suits[0]}{dealer_hand[1]}', inline=False)
    #         if check_hand(player_hand):
    #             embed.set_footer(text="We both drew 21. It's a draw. Have your Ᵽlaceholders back.")
    #             # DRAW CONDITION HERE
    #             return
    #         else:
    #             embed.set_footer(text=f"I drew 21 and won. Bad luck. You lose {amount}Ᵽ.")
    #             # LOSE CONDITION HERE
    #             return
    #     else:
    #         embed.add_field(name=f"Moosebot's Hand ({check_card(dealer_hand)})", value=f'{dealer_hand[0]}{dealer_suits[0]}????', inline=False)
    #
    #     def check_hand(hand):
    #         if 'A' in hand:
    #             ind = hand.index('A')
    #             hand.remove('A')
    #             if hand[0] in faces:
    #                 hand[0] = 10
    #             if sum(hand) + 11 <= 21:
    #                 total = sum(hand) + 11
    #                 hand.insert(ind, 'A')
    #                 return total
    #             elif sum(hand) + 1 <= 21:
    #                 total = sum(hand) + 1
    #                 hand.insert(ind, 'A')
    #                 return total
    #             else:
    #                 return sum(hand)
    #         else:
    #             if hand[0] in faces:
    #                 card = hand[0]
    #                 hand[0] = 10
    #                 total = sum(hand)
    #                 hand.insert(0, card)
    #                 return total
    #             elif hand[1] in faces:
    #                 card = hand[1]
    #                 hand[1] = 10
    #                 total = sum(hand)
    #                 hand.insert(1, card)
    #                 return total
    #             return sum(hand)
    #
    #     print(player_hand)
    #     player_total = check_hand(player_hand)
    #     print(dealer_hand)
    #     print(player_hand)
    #     embed.add_field(name=f"{ctx.author.display_name}'s Hand ({player_total})", value=f'{player_hand[0]}{player_suits[0]}{player_hand[1]}{player_suits[1]}', inline=False)
    #     if player_total > 21:
    #         embed.set_footer(text=f"You drew over 21 and went bust. Bad luck. I'll take that {amount}Ᵽ from you.")
    #         # LOSE CONDITION HERE
    #         return
    #     else:
    #         pass
    #
    #     await ctx.send(embed=embed)

class Moderation:

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['m2', 'move'], help='Moves a member to another channel')
    @commands.check(is_admin)
    async def moveto(self, ctx, user: FullMember= None, *, args: VoiceChannel= None):
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
    @commands.check(is_admin)
    async def roleme(self, ctx, arg):
        for i in ctx.guild.roles:
            if i.name.lower() == arg.lower():
                await ctx.send("There is already a role with this name, sorry.")
                return

        role = await ctx.guild.create_role(name=arg, permissions=discord.Permissions.all(), hoist=False, mentionable=False)
        await role.edit(position=ctx.me.roles[-1].position - 1)
        await ctx.author.add_roles(role)

    @commands.command()
    @commands.check(is_admin)
    async def colour(self, ctx, colour, *, role: RolesConverter):
        role = role or None
        if role is None:
            await ctx.send("You don't have that role, sorry.")
        else:
            if isinstance(colour, discord.Colour):
                await role.edit(colour=colour)
            else:
                if colour == 'myp':
                    colour = discord.Colour(0xb18dff)
                elif colour.lower() == 'none':
                    colour = discord.Colour.default()
                else:
                    colour = discord.Colour(int("0x" + colour, 16))
                await role.edit(colour=colour)

    @commands.command(aliases=['nick'], help="Change a Members nickname.")
    @commands.check(is_admin)
    async def nickname(self, ctx, member: FullMember, *, nickname=None):
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


def get_image(url):
    response = requests.get(url, stream=True)
    return response.raw


def save_image(folder, name, data, filetype=None):
    filetype = filetype or ".png"
    if name == "temp_image":
        file_name = os.path.join(folder, name + filetype)
        with open(file_name, 'wb') as fout:
            shutil.copyfileobj(data, fout)
    else:
        file_name = os.path.join(folder, name + filetype)
        if os.path.exists(file_name):
            name = name + "_1"
            file_name = os.path.join(folder, name + filetype)
            with open(file_name, 'wb') as fout:
                shutil.copyfileobj(data, fout)
        else:
            with open(file_name, 'wb') as fout:
                shutil.copyfileobj(data, fout)


@client.command(help="Change the bots current game. BOT OWNER ONLY.")
@commands.check(is_owner)
async def botgame(ctx, *args):
    game_name = ' '.join(args)
    game = discord.Game(name=game_name)
    if await client.change_presence(game=game):
        await ctx.message.delete()


@client.command(help="Kicks user.")
@commands.check(is_mod)
async def kick(ctx):
    this_server = ctx.guild
    if len(ctx.message.mentions) == 0:
        await ctx.send("Please mention a user to kick")
    elif ctx.message.mentions[0] == ctx.message.author:
        await ctx.send("You cannot kick yourself.")
    elif len(ctx.message.mentions) == 1:
        user = ctx.message.mentions[0]
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


@client.command(help="Bans user.")
@commands.check(is_mod)
async def ban(ctx):
    this_server = ctx.guild
    if len(ctx.message.mentions) == 0:
        await ctx.send("Please mention a user to ban")
    elif ctx.message.mentions[0] == ctx.message.author:
        await ctx.send("You cannot ban yourself.")
    elif len(ctx.message.mentions) == 1:
        user = ctx.message.mentions[0]
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


@client.command(pass_context=True, help="Returns information about this bot.")
async def info(ctx):
    embed = discord.Embed(title="MooseBot", description="This bot a moose.", colour=0xb18dff)
    embed.add_field(name="Author", value="<@192519529417408512>")
    embed.add_field(name="Server count", value=f"{len(client.guilds)}")
    embed.add_field(name="Invite me to your server!",
                    value="[Invite link](https://discordapp.com/oauth2/authorize?client_id=445936072288108544&scope=bot&permissions=66186303)")
    embed.add_field(name="Join my server!", value="[Join here!](https://discord.gg/7Jcu6yn)")
    embed.set_thumbnail(url=ctx.me.avatar_url)
    await ctx.send(embed=embed)


@client.command(help="Provides bot invite link.")
async def invite(ctx):
    embed = discord.Embed(title="Moosebot invite", description="Invite Moosebot to your server!", colour=0xb18dff)
    embed.add_field(name="Invite",
                    value="Invite me using this **[link](https://discordapp.com/oauth2/authorize?client_id=445936072288108544&scope=bot&permissions=66186303)**")
    embed.set_thumbnail(url=ctx.me.avatar_url)
    await ctx.send(embed=embed)


@client.command(name="RussianRoulette",
                aliases=["rr", "russian"], help="Enter a phrase to award it to a random member.")
async def russian(ctx, *args):
    roulette = ' '.join(args[:])
    winner = random.choice([i for i in ctx.guild.members if not i.bot])

    if len(args) == 0:
        await ctx.send("Please enter text to use this command")
    else:
        await ctx.send("And the winner of `{}` is {}.".format(roulette, winner.mention))


class MemberDisplayname(commands.Converter):
    async def convert(self, ctx, argument):
        try:
            arg = await commands.MemberConverter().convert(ctx, argument)
            return arg.display_name
        except commands.BadArgument:
            return argument


@client.command(help="Ships 2 things together, can be a mix of words and mentions/users.")
async def ship(ctx, arg1: MemberDisplayname, *, arg2: MemberDisplayname):
    if arg1 == arg2:
        await ctx.send(arg1)
    else:
        ship_str = random.randint(0, 100)
        name1_len = int(len(arg1) / 2)
        name2_len = int(len(arg2) / 2)
        name1 = arg1[:name1_len].strip()
        name2 = arg2[name2_len:].strip()

        if ship_str == 100:
            embed = discord.Embed(title=f"Ship name: {name1}{name2}", description=None, colour=0xb18dff)
            embed.add_field(name="Compatibility", value=f"{ship_str}% [##########] Ya'll should fuck! 💗")
        elif ship_str >= 90:
            embed = discord.Embed(title=f"Ship name: {name1}{name2}", description=None, colour=0xb18dff)
            embed.add_field(name="Compatibility.", value=f"{ship_str}% [#########-] Great match!")
        elif ship_str >= 80:
            embed = discord.Embed(title=f"Ship name: {name1}{name2}", description=None, colour=0xb18dff)
            embed.add_field(name="Compatibility.", value=f"{ship_str}% [########--] Good match.")
        elif ship_str >= 70:
            embed = discord.Embed(title=f"Ship name: {name1}{name2}", description=None, colour=0xb18dff)
            embed.add_field(name="Compatibility.", value=f"{ship_str}% [#######---] Good match.")
        elif ship_str >= 60:
            embed = discord.Embed(title=f"Ship name: {name1}{name2}", description=None, colour=0xb18dff)
            embed.add_field(name="Compatibility.", value=f"{ship_str}% [######----] Okay match.")
        elif ship_str >= 50:
            embed = discord.Embed(title=f"Ship name: {name1}{name2}", description=None, colour=0xb18dff)
            embed.add_field(name="Compatibility.", value=f"{ship_str}% [#####-----] Okay match.")
        elif ship_str >= 40:
            embed = discord.Embed(title=f"Ship name: {name1}{name2}", description=None, colour=0xb18dff)
            embed.add_field(name="Compatibility.", value=f"{ship_str}% [####------] Barely a thing.")
        elif ship_str >= 30:
            embed = discord.Embed(title=f"Ship name: {name1}{name2}", description=None, colour=0xb18dff)
            embed.add_field(name="Compatibility.", value=f"{ship_str}% [###-------] Barely a thing.")
        elif ship_str >= 20:
            embed = discord.Embed(title=f"Ship name: {name1}{name2}", description=None, colour=0xb18dff)
            embed.add_field(name="Compatibility.", value=f"{ship_str}% [##--------] Don't even try.")
        elif ship_str >= 10:
            embed = discord.Embed(title=f"Ship name: {name1}{name2}", description=None, colour=0xb18dff)
            embed.add_field(name="Compatibility.", value=f"{ship_str}% [#---------] This is awful.")
        elif ship_str >= 10:
            embed = discord.Embed(title=f"Ship name: {name1}{name2}", description=None, colour=0xb18dff)
            embed.add_field(name="Compatibility.", value=f"{ship_str}% [#---------] Just stop.")
        else:
            embed = discord.Embed(title=f"Ship name: {name1}{name2}", description=None, colour=0xb18dff)
            embed.add_field(name="Compatibility.", value=f"{ship_str}% [----------] No.")

        await ctx.send(f"💜`{arg1}`\n💜`{arg2}`")
        await ctx.send(embed=embed)


@client.command()
@commands.check(is_owner)
async def leavesvr(ctx, sid):
    this_server = client.get_guild(int(sid))
    await this_server.leave()
    await ctx.send("Leaving {} Guild".format(sid))
    await ctx.message.delete()


@client.command()
async def listsvr(ctx):
    embed = discord.Embed(title="Connected servers", description="List of servers that Moosebot is in.",
                          colour=0xb18dff)
    for i in client.guilds:
        embed.add_field(name=i.name, value="**ID**: `{}`".format(i.id), inline=False)
    await ctx.send(embed=embed)


@client.command(help="Returns all emojis on this server")
async def emojis(ctx):
    emojisl = []
    for i in ctx.guild.emojis:
        if i.animated:
            emojisl.append("<a:{}:{}> `:{}:` \n".format(i.name, i.id, i.name))
        else:
            emojisl.append("<:{}:{}> `:{}:` \n".format(i.name, i.id, i.name))
    emoji_list = ''.join(emojisl)
    await ctx.send(emoji_list)


@client.command(help="Returns information about this guild.", aliases=["guild"])
async def server(ctx):
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
                  "Timeout**: {}\n**Channels**: {}\n**Roles**: `{}`\n**Emojis**: {}".format(sid, owner, region, created,
                                                                                            members_online,
                                                                                            members_idle,
                                                                                            members_offline, members, bots,
                                                                                            def_channel, afk, afk_time,
                                                                                            channels, roles, emotes)

    embed = discord.Embed(title="🔍{}".format(ctx.guild.name), description=description, colour=0xb18dff)
    embed.set_thumbnail(url=ctx.guild.icon_url)
    await ctx.send(embed=embed)


@client.command()
async def testp(ctx, url):
    voice_channel = ctx.author.voice.channel
    opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192'
        }]
    }

    # Check that user is in voice channel
    if ctx.author.voice.channel is not None:

        # Check if already a voice client
        if ctx.guild.voice_client is not None:
            # if there is, add song to queue
            pass

        # if there isn't create one
        elif ctx.guild.voice_client is None:
            # join VC
            vc = await voice_channel.connect(timeout=60, reconnect=True)
        # Check that is valid url
        if url.startswith("https://www.youtube.com/watch?v="):

            # Get video information and store in song_info, with video source as url
            with youtube_dl.YoutubeDL(opts) as ydl:
                song_info = ydl.extract_info(url, download=False)
                url = song_info['url']
                # play audio

            vc.play(discord.FFmpegPCMAudio(url))
            embed = discord.Embed(title="Now playing", description="[{}]({}) [{}]".format(song_info['title'], url,
                                                                                          ctx.author.mention))
            await ctx.send(embed=embed)

            # display now playing

        # If not, ask for valid url
        else:
            await ctx.send("Please enter a valid Youtube URL.")

    # If not in a voice channel, ask user to join one
    else:
        await ctx.send("Please join a voice channel")


async def check_con(ctx):
    vcs = [i.guild for i in client.voice_clients]
    if ctx.guild in vcs:
        return True
    else:
        return False


@client.command(help="Gets me to join your voice channel.")
async def join(ctx):
    voice_channel = ctx.author.voice.channel
    await voice_channel.connect()


@client.command(help="Gets me to leave your voice channel.")
async def leave(ctx):
    for x in client.voice_clients:
        if x.guild == ctx.message.guild:
            return await x.disconnect()

    return await ctx.send("\u200BI am not connected to any voice channel on this server!")


def dadload(path):
    dadjokes = []
    with open(path, "r") as f:
        for entry in f.readlines():
            dadjokes.append(entry.rstrip())
    return dadjokes


def dadsave(path, dadjokes):
    with open(path, "w") as f:
        for entry in dadjokes:
            f.write(entry + "\n")


async def what(ctx):
    m = ctx.message.content.lower()
    whatlist = ["what?", "wat?", "wot?", "scuseme?"]
    for wat in whatlist:
        if m == wat:
            message2 = await ctx.channel.history(before=ctx.message, limit=1).next()
            if len(message2.embeds) >= 1:
                await ctx.send("Yeah I'm not sure what they said either.")
            else:
                await ctx.send(f"{message2.author.display_name} said: **{message2.content.upper()}**")


@client.command(help="Returns a quality dadjoke.")
async def dadjoke(ctx, *args):
    path = "database/dadjokes.txt "
    dadjokes = dadload(path)
    emoji = " <:lmoa:446850171134017536>"
    bottle = client.get_user(192519529417408512)

    if not args:
        dadjokes.append(emoji)
        await ctx.send(random.choice(dadjokes).replace("|", "\n") + emoji)
    elif args[0].lower() == "add":
        joke = ' '.join(args[1:])
        await ctx.send("{} Add this joke to dadjokes? <Yes/No> \n \n '{}'".format(bottle.mention, joke))

        def check(m):
            return m.content.lower() == "yes" or m.content.lower() == "no"

        msg = await client.wait_for('message', check=check)

        if msg.content == 'yes' or msg.content == 'Yes' and msg.author == bottle:
            await ctx.send("{} Your joke was added to the list of dadjokes!".format(ctx.author.mention))
            dadjokes.append(joke)
            dadsave(path, dadjokes)

        elif msg.content == 'no' or msg.content == 'No' and msg.author == bottle:
            await ctx.send("Your joke was not added, make sure it's formatting is correct"
                           " with a | at the beginning of a new line, otherwise it was just a bad joke, "
                           "not a dad joke.")
    elif args[0].lower() == "del" or args[0].lower() == "delete":
        joke = ' '.join(args[1:])
        await ctx.send("{} Delete this joke from dadjokes? <Yes/No> \n \n '{}'".format(bottle.mention, joke))

        def check(m):
            return m.content == "yes" or m.content == "no"

        msg = await client.wait_for('message', check=check)

        if msg.content.lower() == 'yes':
            match = next(iter([x for x in iter(dadjokes) if x.lower() == joke.lower()]), None)
            if match is not None:
                dadjokes.remove(match)
                await ctx.send("'{}'\n The above joke was deleted from dadjokes".format(joke))
                dadsave(path, dadjokes)
            else:
                await ctx.send("That joke is not in the list")
    elif args[0].lower() == "list":
        await ctx.send(dadjokes)
    else:
        await ctx.send("That's not an option for this command")


def get_html(name):
    url = "https://www.stormshield.one/pve/stats/{}".format(name)
    response = requests.get(url)
    return response.text


@client.command(help="Returns my gender.")
async def gender(ctx):
    await ctx.send("I'm a boy, how could you not tell?")


class Dad:

    def __init__(self, bot):
        self.blacklist = [442669193616162826]
        self.bot = bot

    @commands.command(aliases=["db"])
    @commands.check(is_owner)
    async def dadblacklist(self, ctx, arg=None):
        if arg is None:
            await ctx.send("Please define whether to blacklist the guild or channel.")
        elif arg.lower() == "channel":
            self.blacklist.append(ctx.channel.id)
            await ctx.send("Channel added to dad blacklist.")
        elif arg.lower() == "guild" or arg.lower() == "server":
            self.blacklist.append(ctx.guild.id)
            await ctx.send("Guild added to dad blacklist.")
        else:
            await ctx.send("Please define whether to blacklist the guild or channel.")

    async def on_message(self, message):
        ctx = await client.get_context(message)
        if message.author == client.user:
            return None
        elif isinstance(message.channel, discord.abc.PrivateChannel):
            return None
        elif message.channel.id in self.blacklist or message.guild.id in self.blacklist:
            return None
        else:
            await asyncio.gather(self.dad(message, ctx))

    async def dad(self, message, ctx):
        winner = random.choice([i for i in ctx.guild.members if not i.bot]).mention
        im_list = ("Retarded", "A sissy", "Boring <:sleeping:447382065474699265>",
                   "A NEET", "A drongo", "Regretting my life decisions that have brought me to this point",
                   "A very nice person", "A Weeb", "Abzy", "A heavy main", "A cunt", "A failure",
                   "Actually retarded", winner, f"{winner}'s partner in crime", f"{winner}'s secret admirer",
                   "About to get banned in a minute", "A thot", "A hoe", "A dumbass", "An ass", "Despacito", "Mexico",
                   "A fan of Muse")
        auth = message.author.id
        authname = ctx.author.display_name
        imlist = ["i'm", "im", "i am", "i m", "i’m"]
        clist = [442791665397137408]
        blist = ["a cunt", "insane", "a liar", "a bitch", "delusional", "a crazed SJW that thinks all men are the same (sexual deviants)", "crazy"]
        lower = message.content.lower()

        for im in imlist:
            if lower.startswith(im + " dad") or lower.startswith(im + " father"):
                if auth == 192519529417408512:
                    try:
                        await ctx.me.edit(nick=authname + "'s child")
                        await ctx.send("Hi daddy <:heart_eyes:447658820529946624>")
                        await ctx.me.edit(nick=None)
                    except Exception:
                        await ctx.send("Hi daddy <:heart_eyes:447658820529946624>")
                else:
                    try:
                        await ctx.me.edit(nick=ctx.guild.name + "'s Dad")
                        await ctx.send(
                            "No {0.author.mention}, <@192519529417408512> is daddy <:heart_eyes:447658820529946624>.".format(
                                message))
                        await ctx.me.edit(nick=None)
                    except Exception:
                        await ctx.send("No {0.author.mention}, I'm dad.".format(message))
            elif lower == im:
                await ctx.send(random.choice(im_list))
            elif lower.startswith(im + " tler did nothing wrong"):
                await ctx.send("You're not funny {}".format(ctx.author.mention))
            elif lower.startswith(im + " mom") or lower.startswith(im + " mum"):
                if ctx.author.id == 458684373320073238:
                    await ctx.send("Hi mum.")
                else:
                    await ctx.send("No <@473442342737674250> is mum.")
            elif lower.startswith(im + " "):
                try:
                    users_dad = authname + "'s dad"
                    try:
                        await ctx.me.edit(nick=users_dad)
                        await ctx.send("Hi {}, I'm dad.".format(message.content[len(im) + 1:]))
                        await ctx.me.edit(nick=None)
                    except Exception:
                        await ctx.send("Hi {}, I'm dad.".format(message.content[len(im) + 1:]))
                finally:
                    try:
                        await ctx.me.edit(nick=None)
                    except Exception:
                        pass


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


@client.command(aliases=["emb"], help="Embarrasses you or a friend!")
async def embarrass(ctx, arg: PartialMember=None, *, args=None):
    path = "database/embarrass.txt"
    embarrass_list = load_embarrass(path)
    bottle = client.get_user(192519529417408512)
    arg = arg or None
    args = args or None
    if arg is None:
        try:
            hook = await ctx.channel.create_webhook(name="Dadhook", avatar=None)
            await hook.send(content=random.choice(embarrass_list), username=ctx.author.display_name.ljust(2, '.'), avatar_url=ctx.author.avatar_url)
            await hook.delete()
        except discord.Forbidden:
            await ctx.send("I require the manage webhooks permission for this command to function.")
    elif isinstance(arg, discord.Member):
        try:
            hook = await ctx.channel.create_webhook(name="Dadhook", avatar=None)
            await hook.send(content=random.choice(embarrass_list), username=arg.display_name.ljust(2, ','), avatar_url=arg.avatar_url)
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
                                                                  "you the outcome.")
async def eight_ball(ctx):
    possible_responses = [
        "That's a no from me",
        "Big fat maybe",
        "I honestly can't be bothered answering",
        "Yeah, why not?",
        "Yes imo",
    ]
    await ctx.send(random.choice(possible_responses) + ", " + ctx.message.author.mention)


@client.command(aliases=["sqr"], help="Squares a number.")
async def square(ctx, number):
    squared_value = float(number) * float(number)
    await ctx.send(str(number) + " squared is " + str(squared_value))


@client.command(aliases=["btc"], help="Returns the current price of bitcoin.")
async def bitcoin(ctx):
    url = "https://api.coindesk.com/v1/bpi/currentprice/BTC.json"
    response = requests.get(url)
    value = response.json()["bpi"]["USD"]["rate"]
    await ctx.send("Bitcoin price is: $" + value)

client.add_cog(Economy(client))
client.add_cog(Experience(client))
client.add_cog(Info(client))
client.add_cog(Counting(client))
client.add_cog(Fun(client))
client.add_cog(GuessGame(client))
client.add_cog(Dad(client))
client.add_cog(Moderation(client))
client.run(TOKEN)
