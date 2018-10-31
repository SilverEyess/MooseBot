import random

import discord
import googletrans
import praw
from discord.ext import commands
from googletrans import Translator

from moosebot import MooseBot, converters


class Fun:

    def __init__(self, bot: MooseBot):
        self.bot = bot

    @commands.command(help="Clap👏to👏your👏text. \n`>clap text`")
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
                                                    "your text and it will translate to English. \n`>gt foreign text` \n`gt language text to translate to that language`")
    async def translate(self, ctx, arg1, *, arg2=None):
        google_languages = googletrans.LANGUAGES
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

    @commands.command(
        help="Enter phrases/words separated by commas(,) and I will choose one at random. \n`>choose option1, option 2, option3`")
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

    @commands.command(help="Enter a phrase/word to be γρεεκiφiεδ. \n`>greek text`")
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

    @commands.command(help="Enter a phrase/word to be 丅卄工匚匚工下工乇刀. \n`>thicc text`")
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
        help="Returns :regional_indicator_l: :regional_indicator_e: :regional_indicator_t: :regional_indicator_t: :regional_indicator_i: :regional_indicator_f: :regional_indicator_i: :regional_indicator_e: :regional_indicator_d: text. \n`>letters text`")
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

    @commands.command(help="Returns your message reversed. \n`>reverse text`")
    async def reverse(self, ctx, *, message):
        message = message.split()
        await ctx.send(' '.join(reversed(message)))

    @commands.command(help="Rolls 1, 6 sided dice if given no arguments. Otherwise provide an amount of die, then how "
                           "many sides each one should have for the bot to roll that and sum the rolls. \n`>roll amount sides`")
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

    @commands.command(name="RussianRoulette",
                      aliases=["rr", "russian"],
                      help="Enter a phrase/word to award it to a random member. \n`>rr phrase`")
    async def russian(self, ctx, *args):
        roulette = ' '.join(args[:])
        winner = random.choice([i for i in ctx.guild.members if not i.bot])

        if len(args) == 0:
            await ctx.send("Please enter text to use this command")
        else:
            await ctx.send("And the winner of `{}` is {}.".format(roulette, winner.mention))

    @commands.command(help="Ships 2 things together, can be a mix of words and mentions/users. \n`>ship item1 item2`")
    async def ship(self, ctx, arg1: converters.MemberDisplayName, *, arg2: converters.MemberDisplayName):
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
                embed.add_field(name="Compatibility", value=f"{ship_str}% [##########] Y'all should fuck! 💗")
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

    @commands.command(aliases=["eightball", "8", "ball", "8ball"],
                      help="Simple 8ball, ask a yes/no question and I'll tell "
                           "you the outcome. \n`>8ball question`")
    async def eight_ball(self, ctx):
        possible_responses = [
            "That's a no from me",
            "Big fat maybe",
            "I honestly can't be bothered answering",
            "Yeah, why not?",
            "Yes imo",
        ]
        await ctx.send(random.choice(possible_responses) + ", " + ctx.message.author.mention)
