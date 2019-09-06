import random
import time
from threading import Lock

import motor.motor_asyncio
from PIL import ImageFilter, Image
from discord.ext import commands
from pymongo import MongoClient

from moosebot import MooseBot
from moosebot import converters
from moosebot.cogs import *
from moosebot.utils import *

xplock = Lock()
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
# class Fun:
#     def __init__(self, bot):
#         self.client = bot
#
#     @commands.command(help="Clap👏to👏your👏text. \n`>clap text`")
#     async def clap(self, ctx, *args):
#         clapped = '👏'.join(args)
#         await ctx.send(clapped)
#
#     @commands.command(help="Returns a random spicy maymay.")
#     async def meme(self, ctx):
#         reddit = praw.Reddit(client_id="pok5Y9XHfdwYcA", client_secret="rnch9ufFK2nDpM75NhiDCKzZG_c",
#                              user_agent="SilverEyes_")
#         memes = [i for i in reddit.subreddit('dankmemes').hot(limit=100)]
#         meme = random.choice(memes[1:])
#         embed = discord.Embed(title=meme.title, description=f"[Image]({meme.url})", colour=0xb18dff)
#         embed.set_image(url=meme.url)
#         await ctx.send(embed=embed)
#
#     @commands.command(aliases=['trans', 'gt'], help="This command will translate text. Provide a language as the first "
#                                                     "argument to translate **TO** that language. Otherwise just enter "
#                                                     "your text and it will translate to English. \n`>gt foreign text` \n`gt language text to translate to that language`")
#     async def translate(self, ctx, arg1, *, arg2=None):
#         google_languages = LANGUAGES
#         google_languages_reverse = {v: k for k, v in google_languages.items()}
#         custom_languages = {
#             "baguette": "french",
#             "chink": "zh-cn",
#             "gook": "zh-tw",
#             "paki": "urdu",
#             "indian": "hindi",
#             "swampgerman": "dutch"
#
#         }
#         translator = Translator()
#         if arg1.lower() in google_languages or arg1.lower() in google_languages_reverse:
#             if arg2 is None:
#                 translated_text = translator.translate(arg1)
#                 embed = discord.Embed(title="MooseBot Translator.", description=f"Input text: `{arg1}`",
#                                       colour=0xb18dff)
#                 embed.add_field(name=f"Translated from **English** to **English**:",
#                                 value=f"{translated_text.text}")
#             else:
#                 translated_text = translator.translate(arg2, dest=arg1)
#                 embed = discord.Embed(title="MooseBot Translator.", description=f"Input text: `{arg2}`",
#                                       colour=0xb18dff)
#                 embed.add_field(
#                     name=f"Translated from **English** to **{arg1.title() if arg1 in google_languages_reverse else google_languages[arg1].title()}**:",
#                     value=f"{translated_text.text}")
#             await ctx.send(embed=embed)
#         elif arg1.lower() in custom_languages:
#             translated_text = translator.translate(arg2, dest=custom_languages[arg1])
#             embed = discord.Embed(title="MooseBot Translator.", description=f"Input text: `{arg2}`", colour=0xb18dff)
#             embed.add_field(name=f"Translated from **English** to **{arg1.title()}**:", value=f"{translated_text.text}")
#             await ctx.send(embed=embed)
#         else:
#             if arg2 is None:
#                 input_text = str(arg1)
#             else:
#                 input_text = str(arg1) + " " + str(arg2)
#             translated_text = translator.translate(input_text)
#             if translated_text.src in google_languages:
#                 language = google_languages[translated_text.src].title()
#             elif translated_text.src in google_languages_reverse:
#                 language = google_languages_reverse[translated_text.src].title()
#             embed = discord.Embed(title="MooseBot Translator.", description=f"Input text: `{input_text}`",
#                                   colour=0xb18dff)
#             embed.add_field(
#                 name=f"Translated from **{google_languages[translated_text.src.lower()].title() if translated_text.src.lower() in google_languages else google_languages_reverse[translated_text.src.lower()].title()}** to English:",
#                 value=f"{translated_text.text}")
#             await ctx.send(embed=embed)
#
#     @commands.command(
#         help="Enter phrases/words separated by commas(,) and I will choose one at random. \n`>choose option1, option 2, option3`")
#     async def choose(self, ctx, *choices: str):
#         choices = ' '.join(choices)
#         choices = choices.split(',')
#         choice = random.randint(0, len(choices))
#         if len(choices) == 1:
#             await ctx.send("Please separate the choices with a comma `>choose a, b, c`.")
#         else:
#             await ctx.send(f"I choose `{choices[choice]}`.")
#
#     @commands.command(help="Returns a random face.")
#     async def face(self, ctx):
#         choices = ("🌚 👅 🌚", "🌐➖🌐", "<:eye_in_speech_bubble:463956840905048066> ♨ "
#                                         "<:eye_in_speech_bubble:463956840905048066>", "🌕 ♨ 🌕", "┌( ಠ_ಠ)┘",
#                    "^-^", "OwO", "👌 👅 👌", "👅 👁 👅", "◔ ⌣ ◔", "◔̯◔",
#                    "<:wobo:461535897666584586> ➖ <:wobo:461535897666584586>", "⭕〰⭕", "⭕ 💋 ⭕", "ง ͠° ل͜ °)ง", "๏̯͡๏﴿",
#                    "༼ ºººººل͟ººººº ༽", "༼ つ ◕_◕ ༽つ", "༼ʘ̚ل͜ʘ̚༽", "ლ(´ڡ`ლ)", "ლ(́◉◞౪◟◉‵ლ)", "ლ(ಠ益ಠლ)", "╚(ಠ_ಠ)=┐",
#                    "<:fat:428937630009262090> ➖ <:fat:428937630009262090>", "✌(-‿-)✌", "\_(ʘ_ʘ)_/", "ʕ•ᴥ•ʔ", "- o -",
#                    "o - o", "ಠ▃ಠ", "ಠ╭╮ಠ", "ಥ_ಥ", "ಥ◡ಥ", "ಥ﹏ಥ", "ಥдಥ", ">﹏>", ">﹏<", "<﹏<", "༼ つ  >﹏<༽つ")
#         await ctx.send(random.choice(choices))
#
#     @commands.command(help="Enter a phrase/word to be γρεεκiφiεδ. \n`>greek text`")
#     async def greek(self, ctx, *, arg=None):
#         arg = arg or None
#         if arg is None:
#             await ctx.send("Please provide a word or phrase to be γρεεκiφiεδ.")
#         else:
#             greekMap = {
#                 'a': 'α',
#                 'b': 'β',
#                 'c': 'κ',
#                 'd': 'δ',
#                 'e': 'ε',
#                 'f': 'φ',
#                 'g': 'γ',
#                 'h': 'η',
#                 'j': 'ζ',
#                 'k': 'κ',
#                 'l': 'λ',
#                 'm': 'μ',
#                 'n': 'ν',
#                 'o': 'ο',
#                 'p': 'π',
#                 'q': 'κ',
#                 'r': 'ρ',
#                 's': 'σ',
#                 't': 'τ',
#                 'u': 'υ',
#                 'v': 'β',
#                 'w': 'ω',
#                 'y': 'υ',
#                 'x': 'ξ',
#                 'z': 'ζ'
#             }
#             newtext = []
#             for i in arg:
#                 if i.lower() in greekMap:
#                     newtext.append(greekMap[i.lower()])
#                 else:
#                     newtext.append(i)
#             greekified = ''.join(newtext)
#             await ctx.send(greekified)
#
#     @commands.command(help="Enter a phrase/word to be 丅卄工匚匚工下工乇刀. \n`>thicc text`")
#     async def thicc(self, ctx, *, arg=None):
#         arg = arg or None
#         if arg is None:
#             await ctx.send("Please enter a word or phrase to be 丅卄工匚匚工下工乇刀.")
#         else:
#             thiccMap = {
#                 "a": "卂",
#                 "b": "乃",
#                 "c": "匚",
#                 "d": "刀",
#                 "e": "乇",
#                 "f": "下",
#                 "g": "厶",
#                 "h": "卄",
#                 "i": "工",
#                 "j": "丁",
#                 "k": "长",
#                 "l": "乚",
#                 "m": "从",
#                 "n": "\uD841\uDE28",
#                 "o": "口",
#                 "p": "尸",
#                 "q": "㔿",
#                 "r": "尺",
#                 "s": "丂",
#                 "t": "丅",
#                 "u": "凵",
#                 "v": "リ",
#                 "w": "山",
#                 "x": "乂",
#                 "y": "丫",
#                 "z": "乙"
#             }
#             newtext = []
#             for i in arg:
#                 if i.lower() in thiccMap:
#                     newtext.append(thiccMap[i.lower()])
#                 else:
#                     newtext.append(i)
#             thiccified = ''.join(newtext)
#             await ctx.send(thiccified)
#
#     @commands.command(
#         help="Returns :regional_indicator_l: :regional_indicator_e: :regional_indicator_t: :regional_indicator_t: :regional_indicator_i: :regional_indicator_f: :regional_indicator_i: :regional_indicator_e: :regional_indicator_d: text. \n`>letters text`")
#     async def letters(self, ctx, *, arg=None):
#         arg = arg or None
#         if arg is None:
#             await ctx.send(
#                 "Please provide a word or phrase to be :regional_indicator_l: :regional_indicator_e: :regional_indicator_t: :regional_indicator_t: :regional_indicator_i: :regional_indicator_f: :regional_indicator_i: :regional_indicator_e: :regional_indicator_d:.")
#         else:
#             lettersMap = {
#                 "a": "🇦",
#                 "b": "🇧",
#                 "c": "🇨",
#                 "d": "🇩",
#                 "e": "🇪",
#                 "f": "🇫",
#                 "g": "🇬",
#                 "h": "🇭",
#                 "i": "🇮",
#                 "j": "🇯",
#                 "k": "🇰",
#                 "l": "🇱",
#                 "m": "🇲",
#                 "n": "🇳",
#                 "o": "🇴",
#                 "p": "🇵",
#                 "q": "🇶",
#                 "r": "🇷",
#                 "s": "🇸",
#                 "t": "🇹",
#                 "u": "🇺",
#                 "v": "🇻",
#                 "w": "🇼",
#                 "x": "🇽",
#                 "y": "🇾",
#                 "z": "🇿",
#                 "0": ":zero:",
#                 "1": ":one:",
#                 "2": ":two:",
#                 "3": ":three:",
#                 "4": ":four:",
#                 "5": ":five:",
#                 "6": ":six:",
#                 "7": ":seven:",
#                 "8": ":eight:",
#                 "9": ":nine:",
#                 "?": "❔",
#                 "!": "❕"
#             }
#             newtext = []
#             for i in arg:
#                 if i.lower() in lettersMap:
#                     newtext.append(lettersMap[i.lower()])
#                 else:
#                     newtext.append(i)
#             lettered = ' '.join(newtext)
#             if len(lettered) >= 2048:
#                 new_letters = lettered.split(" ")
#                 await ctx.send("Yo your message is too long, shorten it until I fix a workaround for this")
#             else:
#                 await ctx.send(lettered)
#
#     @commands.command(aliases=['ct'], help="Flip a coin.")
#     async def cointoss(self, ctx):
#         choices = ('Heads!', 'Tails!')
#         await ctx.send(random.choice(choices))
#
#     @commands.command(help="Returns your message reversed. \n`>reverse text`")
#     async def reverse(self, ctx, *, message):
#         message = message.split()
#         await ctx.send(' '.join(reversed(message)))
#
#     @commands.command(help="Rolls 1, 6 sided dice if given no arguments. Otherwise provide an amount of die, then how "
#                            "many sides each one should have for the bot to roll that and sum the rolls. \n`>roll amount sides`")
#     async def roll(self, ctx, *choices: int):
#         die_rolls = []
#
#         def roll_die(sides, amount):
#             throws = 0
#             while throws < amount:
#                 throws += 1
#                 roll = random.randint(1, sides)
#                 yield roll
#
#         if len(choices) == 0:
#             die_amount = 1
#             die_sides = 6
#         else:
#             die_amount = choices[0]
#             die_sides = choices[1]
#         if die_amount == 0 or die_sides == 0:
#             await ctx.send("You need to throw at least 1 die with at least 1 side.")
#         elif die_amount < 21 and die_amount != 1:
#             for i in roll_die(die_sides, die_amount):
#                 die_rolls.append(i)
#             await ctx.trigger_typing()
#             await ctx.send(f"You rolled {die_amount}, {die_sides} sided die and got the following rolls: "
#                            f"{''.join(str(die_rolls))}. For a total of {sum(die_rolls)}")
#         else:
#             for i in roll_die(die_sides, die_amount):
#                 die_rolls.append(i)
#             await ctx.trigger_typing()
#             await ctx.send(f"You rolled {die_amount}, {die_sides} sided die. For a total of {sum(die_rolls)}")
#
#     @roll.error
#     async def roll_error(self, ctx, error):
#         if isinstance(error, commands.CommandInvokeError):
#             await ctx.trigger_typing()
#             await ctx.send("Please use a number that is more than 1 for both arguments. "
#                            "Or no arguments to roll 1, 6 sided die.")
#         else:
#             await ctx.send(error)
#
#
# class GuessGame:
#
#     def __init__(self, bot):
#         self.client = bot
#
#     async def get_input(self, ctx, datatype, error=''):
#         while True:
#             try:
#                 message = await self.client.wait_for('message', check=lambda message: message.author is ctx.author,
#                                                      timeout=60)
#                 message = datatype(message.content)
#                 return message
#             except Exception:
#                 await ctx.send(error)
#
#     async def gameover(self, ctx, funct):
#         await ctx.send("Do you want to play again? (**Yes**/**No**)")
#         self.message = await self.get_input(ctx, str)
#         self.message = self.message.lower()
#
#         if self.message == 'yes' or self.message == 'y':
#             await funct()
#         elif self.message == 'no' or self.message == 'n':
#             await ctx.send("Thanks for playing!")
#         else:
#             await self.gameover(ctx, funct)
#
#     @commands.command(help="Guess the number game.")
#     async def guess(self, ctx):
#
#         async def play():
#             channel = ctx.channel
#             await ctx.send("Guess a number between 1 and 100.")
#             error = "Please enter a number."
#             guess = await self.get_input(ctx, int, error)
#             answer = random.randint(1, 100)
#             counter = 0
#
#             while guess != answer:
#                 counter += 1
#                 if guess > answer:
#                     await ctx.send("{} your guess of `{}` is too high! Try again".format(ctx.author.mention, guess))
#                     guess = await self.get_input(ctx, int, error)
#                 else:
#                     await ctx.send("{} your guess of `{}` is too low! Try again".format(ctx.author.mention, guess))
#                     guess = await self.get_input(ctx, int, error)
#             else:
#                 if counter <= 1:
#                     await ctx.send("Congratulations! You got it on the first attempt!")
#                 else:
#                     await ctx.send(f"Congratulations! It took you {counter} tries to guess the correct number.")
#                 await self.gameover(ctx, play)
#
#         await play()
#
#     @commands.command(help="Rock paper scissors game.")
#     async def rps(self, ctx, amount=None):
#         user = str(ctx.author.id)
#         amount = amount or None
#         if amount is None:
#             amount = 1
#         elif amount == 'all':
#             amount = int(db.money.find_one({'userid': user})['balance'])
#         if amount == 'all':
#             amount = db.money.find_one({'userid': user})['balance']
#         if amount <= 0:
#             await ctx.send("You need to bet at least 1Ᵽ to play.")
#
#         async def play():
#             await ctx.send("Let's play rock, paper, scissors. Select your weapon:")
#             choices = ('rock', 'paper', 'scissors')
#             computer = choices[random.randint(0, 2)]
#             player = await self.get_input(ctx, str)
#             player = player.lower()
#             if player == 'r':
#                 player = 'rock'
#             elif player == 's':
#                 player = 'scissors'
#             elif player == 'p':
#                 player = 'paper'
#             else:
#                 player = player
#
#             beats = {'rock': ['paper'],
#                      'paper': ['scissors'],
#                      'scissors': ['rock']}
#
#             if computer and player in choices:
#                 if computer == player:
#                     await ctx.send(f"**Tie!** You both chose {computer.title()}. You lose no Ᵽlaceholders.")
#                     await self.gameover(ctx, play)
#                 elif player in beats[computer]:
#                     await ctx.send(
#                         f"**You win!** Moosebot chose: {computer.title()}, and you chose: {player.title()}.You won {amount}Ᵽ.")
#                     db.money.update({'userid': str(ctx.author.id)}, {'$inc': {'balance': amount}})
#                     await self.gameover(ctx, play)
#                 else:
#                     await ctx.send(
#                         f"**You lose!** Moosebot chose: {computer.title()}, and you chose: {player.title()}.You lost {amount}Ᵽ.")
#                     db.money.update({'userid': str(ctx.author.id)}, {'$inc': {'balance': -amount}})
#                     await self.gameover(ctx, play)
#             else:
#                 await play()
#
#         await play()
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
class Experience:

    def __init__(self, bot):
        self.bot = bot

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
        server = str(ctx.guild.id)
        order = 1

        lvls = {}
        async for i in db.xp.find_one({'serverid': server}):
            try:
                user = client.get_user(int(i))
                lvls[user.id] = await db.xp.find_one({'serverid': server})[i]
            except Exception:
                continue
        lvls = sorted(lvls.items(), key=lambda kv: kv[1], reverse=True)
        eligable = []
        for i in lvls:
            try:
                eligable.append(
                    f'▫{order}. **{client.get_user(i[0]).display_name}**: {db.lvl.find_one({"serverid": server})[str(i[0])] if not None else "0"} `({str(i[1])} exp)` \n')
                order += 1
            except Exception:
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
        if leftover != 0:
            pages.append(eligable[-leftover:])
            pagesamount += 1
        curpage = 0
        foot_page = 1
        embed = discord.Embed(title="Experience Leaderboard.", description=''.join(pages[curpage]), colour=0xb18dff)
        embed.set_footer(text=f'Page({foot_page}/{pagesamount})')
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
                        embed = discord.Embed(title='Experience Leaderboard.', description=''.join(pages[curpage - 1]),
                                              colour=0xb18dff)
                        embed.set_footer(text=f'Page ({foot_page}/{pagesamount})')
                        await msg.edit(embed=embed)
                        curpage -= 1
                    await msg.remove_reaction(emoji='◀', member=ctx.author)
                elif str(reaction.emoji) == '▶' and user == ctx.author:
                    if curpage == pagesamount - 1:
                        await msg.remove_reaction(emoji='▶', member=ctx.author)
                        continue
                    else:
                        foot_page += 1
                        embed = discord.Embed(title='Experience Leaderboard.', description=''.join(pages[curpage + 1]),
                                              colour=0xb18dff)
                        embed.set_footer(text=f'Page ({foot_page}/{pagesamount})')
                        await msg.edit(embed=embed)
                        curpage += 1
                    await msg.remove_reaction(emoji='▶', member=ctx.author)

    @commands.command(aliases=['lvl', 'rank'], help='Check your current xp and level standings.')
    async def level(self, ctx, member: converters.FullMember = None):
        server = str(ctx.guild.id)
        eligable = {}
        async for i in db.lvl.find_one({'serverid': server}):
            try:
                if i == '_id' or i == 'serverid':
                    continue
                else:
                    client.get_user(int(i))
                    eligable[i] = await db.lvl.find_one({'serverid': server})[i]
            except AttributeError:
                continue
        level_list2 = sorted(eligable.items(), key=lambda kv: kv[1], reverse=True)
        member = member or None
        if member is None:
            user = str(ctx.author.id)
            member = ctx.author
        elif isinstance(member, discord.Member):
            try:
                client.get_user(member.id)
                user = str(member.id)

            except AttributeError:
                await ctx.send("That user isn't on this server anymore.")
        else:
            await ctx.send("That isn't a person.")
        rank = [i for i in level_list2 if i[0] == user]
        nextlvl = f'{user}_nextlevel'
        try:
            person = await db.xp.find_one({'serverid': server})[user]
            nextlevel = await db.xp.find_one({'serverid': server})[nextlvl]
            xp = f"{person}/{nextlevel}"
        except KeyError:
            xp = await db.xp.find_one({'serverid': server})[user]
        level = await db.lvl.find_one({'serverid': server})[user]
        embed = discord.Embed(title=f"{member.display_name}'s level details",
                              description=f"**Rank:** {level_list2.index(rank[0]) + 1} \n**Level:** {level}\n**Experience:** {xp}",
                              colour=0xb18dff)
        await ctx.send(embed=embed)

    @commands.command(aliases=['gvxp'], help='Bot author only command.')
    @commands.check(is_owner)
    async def givexp(self, ctx, user: converters.FullMember = None, *, args: int):
        user = user or None
        args = args or None
        if user is None:
            await ctx.send("Please tell me who to give xp to.")
        elif args is None:
            await ctx.send(f"Please tell me how much xp to give to `{user.display_name}`.")
        else:
            await db.xp.update_one({'serverid': str(ctx.guild.id)}, {'$inc': {str(user.id): args}})
            await ctx.send(f"{args} xp successfully given to {user.display_name}.")

    @commands.command(aliases=['rmvxp'], help='Bot author only command.')
    @commands.check(is_owner)
    async def removexp(self, ctx, user: converters.FullMember = None, *, args):
        user = user or None
        args = args or None
        if user is None:
            await ctx.send("Please tell me who to take xp from.")
        elif args is None:
            await ctx.send(f"Please tell me how much xp to take from `{user.display_name}`.")
        else:
            if args == 'all' or args == '*':
                beforexp = await db.xp.find_one({'userid': str(user.id)})
                if beforexp is None:
                    await ctx.send("This user had no xp to take...")
                else:
                    await db.xp.update_one({'userid': str(user.id)}, {'$set': {'experience': 0}})
                    await ctx.send(f"{beforexp} xp successfully taken from {user.display_name}.")
            else:
                await db.xp.update_one({'userid': str(user.id)}, {'$inc': {'experience': -int(args)}})
                await ctx.send(f"{args} xp successfully taken from {user.display_name}.")

    @commands.command()
    async def test2(self, ctx):
        for i in client.guilds:
            if i.id == 497565873570316289:
                for x in i.members():
                    db.money.update_one({'userid': str(x.id)}, {'$inc': {'balance': 500}}, True)

    async def grantxp(self, message):
        xplock.acquire()
        xpamount = random.randint(1, 10)
        try:
            author = str(message.author.id)
            await db.xp.update_one({'serverid': str(message.guild.id)}, {'$inc': {author: xpamount}}, True)
            userxp = await db.xp.find_one({'serverid': str(message.guild.id)})
            userxp = userxp[author]
            if userxp is not None:
                level_amount = 100
                newlevel = 0
                levelxp = 0
                while levelxp < userxp:
                    if newlevel < 50:
                        level_amount = int(level_amount * 0.04) + level_amount
                    else:
                        level_amount = level_amount
                    levelxp += int(level_amount)
                    newlevel += 1
                    if levelxp > userxp:
                        newlevel -= 1
                userlvl = await db.lvl.find_one({'serverid': str(message.guild.id)})
                userlvl = userlvl[author]
                await db.xp.update_one({'serverid': str(message.guild.id)}, {
                    '$set': {f'{author}_nextlevel': levelxp + (int((level_amount * 0.04) + level_amount))}}, True)
                if author not in await db.lvl.find_one({'serverid': str(message.guild.id)}):
                    await db.lvl.update_one({'serverid': str(message.guild.id)}, {'$set': {author: newlevel}}, True)
                elif newlevel != userlvl:
                    await message.channel.send(
                        f"Congratulations {message.author.mention} you leveled up to level {newlevel}!")
                    await db.lvl.update_one({'serverid': str(message.guild.id)}, {'$set': {author: newlevel}}, True)
        finally:
            xplock.release()


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
# class MemberDisplayname(commands.Converter):
#     async def convert(self, ctx, argument):
#         try:
#             arg = await commands.MemberConverter().convert(ctx, argument)
#             return arg.display_name
#         except commands.BadArgument:
#             return argument
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
# @client.command()
# async def listsvr(ctx):
#     embed = discord.Embed(title="Connected servers", description="List of servers that Moosebot is in.",
#                           colour=0xb18dff)
#     for i in client.guilds:
#         embed.add_field(name=i.name, value="**ID**: `{}`".format(i.id), inline=False)
#     await ctx.send(embed=embed)
#
#
# @client.command(help="Returns all emojis on this server")
# async def emojis(ctx):
#     emojisl = []
#     for i in ctx.guild.emojis:
#         if i.animated:
#             emojisl.append("<a:{}:{}> `:{}:` \n".format(i.name, i.id, i.name))
#         else:
#             emojisl.append("<:{}:{}> `:{}:` \n".format(i.name, i.id, i.name))
#     emoji_list = ''.join(emojisl)
#     await ctx.send(emoji_list)
#
#
# @client.command(help="Returns information about this guild.", aliases=["guild"])
# async def server(ctx):
#     sid = ctx.guild.id
#     owner = ctx.guild.owner.mention
#     region = ctx.guild.region
#     created = ctx.guild.created_at.strftime("%d/%m/%Y %I:%M:%S")
#     members = len([i for i in ctx.guild.members if not i.bot])
#     bots = len([i for i in ctx.guild.members if i.bot])
#     members_offline = len([i for i in ctx.guild.members if i.status == discord.Status.offline])
#     members_online = len([i for i in ctx.guild.members if i.status == discord.Status.online])
#     members_idle = len(
#         [i for i in ctx.guild.members if i.status == discord.Status.idle or i.status == discord.Status.dnd])
#     def_channel = "#{}".format(ctx.guild.system_channel)
#     afk = ctx.guild.afk_channel
#     afk_time = "{} minutes".format(ctx.guild.afk_timeout / 60)
#     text_channels = len(ctx.guild.text_channels)
#     voice_channels = len(ctx.guild.voice_channels)
#     channels = "`{}` Text | `{}` Voice | **{}** Total".format(text_channels, voice_channels,
#                                                               text_channels + voice_channels)
#     roles = len(ctx.guild.roles)
#     emotes = ''.join(map(str, ctx.guild.emojis))
#     description = "**ID**: `{}`\n**Owner**: {}\n**Region**: __{}__\n**Created**: `{}` \n**Users**: `{}` Online | `{}`" \
#                   " Away | `{}` Offline | **{}** Total(+{} bots)\n**Default Channel**: {}\n**AFK Channel**: #{}\n**AFK " \
#                   "Timeout**: {}\n**Channels**: {}\n**Roles**: `{}`\n**Emojis**: {}".format(sid, owner, region, created,
#                                                                                             members_online,
#                                                                                             members_idle,
#                                                                                             members_offline, members,
#                                                                                             bots,
#                                                                                             def_channel, afk, afk_time,
#                                                                                             channels, roles, emotes)
#
#     embed = discord.Embed(title="🔍{}".format(ctx.guild.name), description=description, colour=0xb18dff)
#     embed.set_thumbnail(url=ctx.guild.icon_url)
#     await ctx.send(embed=embed)
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






@client.command(
    help="Returns a quality dadjoke. Or try to add/remove jokes(If bot author on your server) \n`>dadjoke add/remove joke`")
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


#
#
client.add_cog(Pet(moose))
client.add_cog(Shop(moose))
client.add_cog(Economy(moose))
# client.add_cog(Experience(client))
client.add_cog(Info(client))
client.add_cog(Counting(moose))
# client.add_cog(Counting(client))
# client.add_cog(Fun(client))
# client.add_cog(GuessGame(client))
client.add_cog(Dad(moose))
client.add_cog(Moderation(moose))
client.run(token)
