import asyncio
import random
from threading import Lock

import discord
import googletrans
import praw
from discord.ext import commands
from discord.ext.commands import Cog
from googletrans import Translator

from moosebot import MooseBot, converters


class Fun(Cog):

    def __init__(self, bot: MooseBot):
        self.bot = bot
        self.lock = Lock()
        self.respecton = 0
        self.db = bot.database.db

    @Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.client.user:
            return
        elif message.content == "+f" and self.respecton == 0:
            await asyncio.gather(self.respects(message))
        else:
            await asyncio.gather(self.swear_jar(message), self.china(message))

    async def respects(self, message):
        numbers = {"1": u"1\u20e3",
                   "2": u"2\u20e3",
                   "3": u"3\u20e3",
                   "4": u"4\u20e3",
                   "5": u"5\u20e3",
                   "6": u"6\u20e3",
                   "7": u"7\u20e3",
                   "8": u"8\u20e3",
                   "9": u"9\u20e3",
                   "0": u"0\u20e3"
                   }

        self.respecton = 1
        resp = await message.channel.send(f"{message.author.mention} has paid respects. Type `+f` to also pay respect.")
        await resp.add_reaction(u"1\u20e3")
        flist = [message.author.id]

        while True:

            def check(m):
                return m.channel == message.channel and m.author.id not in flist and m.content == "+f"
            try:
                msg = await self.bot.client.wait_for('message', check=check, timeout=10)
                flist.append(msg.author.id)
                amount = list(str(len(flist)))
                reacts = []
                await resp.clear_reactions()
                for i in amount:
                    if i in numbers:
                        reacts.append(numbers[i])
                for i in reacts:
                    await resp.add_reaction(i)
            except asyncio.TimeoutError:
                break
        await message.channel.send(f"`{len(flist)}` people paid respects.")
        self.respecton = 0

    @commands.command(help="Clap👏to👏your👏text. \n`>clap text`")
    async def clap(self, ctx, *, args=None):
        args = args or None

        if args is None:
            await ctx.send("Please👏provide👏a👏message👏to👏be👏clappified.")
        else:
            clapped = '👏'.join(args.split())
            await ctx.send(clapped)

    async def china(self, message):
        copypasta = "动态网自由门 天安門 天安门 法輪功 李洪志 Free Tibet 六四天安門事件 The Tiananmen Square protests of 1989 天安門大屠殺 The Tiananmen Square Massacre 反右派鬥爭 The Anti-Rightist Struggle 大躍進政策 The Great Leap Forward 文化大革命 The Great Proletarian Cultural Revolution 人權 Human Rights 民運 Democratization 自由 Freedom 獨立 Independence 多黨制 Multi-party system 台灣 臺灣 Taiwan Formosa 中華民國 Republic of China 西藏 土伯特 唐古特 Tibet 達賴喇嘛 Dalai Lama 法輪功 Falun Dafa 新疆維吾爾自治區 The Xinjiang Uyghur Autonomous Region 諾貝爾和平獎 Nobel Peace Prize 劉暁波 Liu Xiaobo 民主 言論 思想 反共 反革命 抗議 運動 騷亂 暴亂 騷擾 擾亂 抗暴 平反 維權 示威游行 李洪志 法輪大法 大法弟子 強制斷種 強制堕胎 民族淨化 人體實驗 肅清 胡耀邦 趙紫陽 魏京生 王丹 還政於民 和平演變 激流中國 北京之春 大紀元時報 九評論共産黨 獨裁 專制 壓制 統一 監視 鎮壓 迫害 侵略 掠奪 破壞 拷問 屠殺 活摘器官 誘拐 買賣人口 遊進 走私 毒品 賣淫 春畫 賭博 六合彩 天安門 天安门 法輪功 李洪志 Winnie the Pooh 劉曉波动态网自由门"
        if message.author.bot:
            return

        elif "china" in message.content.lower():
            await message.channel.send(copypasta)

    async def swear_jar(self, message):
        swear_list = ['fuck', 'shit', 'piss', 'bitch', 'cunt', 'bastard', 'dick', 'minion', 'cock', 'fag', 'hell', 'bussy', 'shart', 'boy2boy', 'ead', 'spearchucker', 'm2m', 'girl2girl', 'boy 4 boy', 'girl 4 girl', 'ass', 'prick', 'whore', 'arse', 'ballsucker']
        message_list = ['Allah is watching.', 'Allah is disappointed.', 'Allah has sacrificed your virgins.', "This is a good extremist Muslim server."]
        serverid = message.guild.id
        server = await self.db.server.find_one({'serverid': str(serverid)})
        if message.guild is None:
            return

        if server is None:
            await self.db.server.update_one({'serverid': str(serverid)}, {'$set': {'swear_jar': 0}}, True)
        swears = [i for i in swear_list if i in message.content.lower()]

        for x in swears:
            await self.db.server.update_one({'serverid': str(serverid)}, {'$inc': {'swear_jar': 1}}, True)
            await self.db.money.update_one({'userid': str(message.author.id)}, {'$inc': {'swears': 1}})
            jar = await self.db.server.find_one({'serverid': str(serverid)})
            swear_count = jar['swear_jar']
            if swear_count < 100:
                await message.channel.send(f"Swear counter: {swear_count} \n{random.choice(message_list)}")

            elif swear_count > 100:
                divided = swear_count / 100
                if divided.is_integer():
                    await message.channel.send(f"Swear counter: {swear_count} \n{random.choice(message_list)}")
                elif str(swear_count).endswith('69'):
                    await message.channel.send(f"Swear counter: {swear_count} \n{random.choice(message_list)}")

    @commands.command()
    async def howlong(self, ctx, *, user: converters.FullMember = None):
        letters = {"a": 1.1,
                   "b": 1.3,
                   "c": 1.1,
                   "d": 1.2,
                   "e": 1,
                   "f": 1.4,
                   "g": 1.7,
                   "h": 1.3,
                   "i": 1.1,
                   "j": 2.3,
                   "k": 2,
                   "l": 1.3,
                   "m": 1.2,
                   "n": 0.9,
                   "o": 1,
                   "p": 0.7,
                   "q": 2.8,
                   "r": 0.8,
                   "s": 0.9,
                   "t": 0.9,
                   "u": 1.3,
                   "v": 1.4,
                   "w": 1.3,
                   "x": 2.6,
                   "y": 1.4,
                   "z": 2.5,
                   "0": 0.5,
                   "1": 1,
                   "2": 0.5,
                   "3": 1.2,
                   "4": 1.1,
                   "5": 0.8,
                   "6": 2,
                   "7": 0.3,
                   "8": 1.3,
                   "9": 1.4,
                   "Τ": 9.6,
                   "ρ": 3.4,
                   "ε": 2.7,
                   "γ": 4,
                   "α": 1,
                   "σ": 1.2,
                   "τ": 1.3
                   }
        user = user or None
        if user is None:
            uid = ctx.author.id
            un = ctx.author
        else:
            if not isinstance(user, discord.Member):
                await ctx.send("You need to mention a user or give no input.")
                return
            else:
                uid = user.id
                un = user

        def calc(unit):
            size = 0
            for i in unit:
                if i in letters:
                    size += float(letters[i])
            size = f"{size:.1f}"
            return size
        length = calc(un.name)
        if length == "0.0":
            length = calc(str(un.display_name))
            if length == "0.0":
                length = calc(str(un.id))
        if uid == int(MooseBot.owner):
            await ctx.send(f"{'You have' if user is None else f'{user.display_name} has'} an optimally lengthed wiener at {length}cm long.")
        else:
            await ctx.send(f"{'You have' if user is None else f'{user.display_name} has'} a {length}cm long wiener.")

    @commands.command(help="Returns a random spicy maymay.", hidden=True)
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

    def load(self, path):
        result = []
        with open(path, "r") as f:
            for entry in f.readlines():
                result.append(entry.rstrip())
        return result

    @commands.command()
    async def amicool(self, ctx):
        emojies = ['😎', '🙂']
        chances = random.randint(1, 10)
        current = 0
        choice = random.randint(0, 1)
        msg = "You are..."
        message = await ctx.send(msg)
        while current < chances:
            current += 1
            if choice == 0:
                choice = 1
                msg = f"You are uncool {emojies[choice]}"
                await message.edit(content=msg)
                await asyncio.sleep(1)
            else:
                choice = 0
                msg = f"You are cool {emojies[choice]}"
                await message.edit(content=msg)
                await asyncio.sleep(1)

    @commands.command()
    async def sponsor(self, ctx):
        choices = self.load('database/sponsors.txt')
        choice = random.choice(choices).replace("|", "\n")
        embed = discord.Embed(title='Please pause for this important message from our sponsors.', description=choice, colour=0xb18dff)
        embed.set_thumbnail(url='https://library.kissclipart.com/20180903/gpe/kissclipart-money-vector-clipart-money-clip-art-795916cc43a26bc2.jpg')
        await ctx.send(embed=embed)

    @commands.command(
        help="Enter phrases/words separated by commas(,) and I will choose one at random. \n`>choose option1, option 2, option3`")
    async def choose(self, ctx, *choices: str):
        choices = ' '.join(choices)
        choices = choices.split(',')
        choice = random.choice(choices)
        if len(choices) == 1:
            await ctx.send("Please separate the choices with a comma `>choose a, b, c`.")
        else:
            await ctx.send(f"I choose `{choice}`.")

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
    async def ship(self, ctx, arg1: converters.MemberDisplayName = None, *, arg2: converters.MemberDisplayName = None):
        if arg1 is None:
            arg1 = ctx.author.display_name
            arg2 = random.choice([i.display_name for i in ctx.guild.members])
        elif arg2 is None:
            arg2 = random.choice([i.display_name for i in ctx.guild.members])
        elif arg1 == arg2:
            await ctx.send(arg1)
            await ctx.send(f"You just shipped '{arg1}' with '{arg1}' what did you expect?")
            return

        ship_value = random.randint(0, 100)
        name1_len = int(len(arg1) / 2)
        name2_len = int(len(arg2) / 2)
        name1 = arg1[:name1_len].strip()
        name2 = arg2[name2_len:].strip()

        if ship_value == 100:
            embed = discord.Embed(title=f"Ship name: {name1}{name2}", description=None, colour=0xb18dff)
            embed.add_field(name="Compatibility", value=f"{ship_value}% [##########] Y'all should fuck! 💗")
        elif ship_value >= 90:
            embed = discord.Embed(title=f"Ship name: {name1}{name2}", description=None, colour=0xb18dff)
            embed.add_field(name="Compatibility.", value=f"{ship_value}% [#########-] Great match!")
        elif ship_value >= 80:
            embed = discord.Embed(title=f"Ship name: {name1}{name2}", description=None, colour=0xb18dff)
            embed.add_field(name="Compatibility.", value=f"{ship_value}% [########--] Good match.")
        elif ship_value >= 70:
            embed = discord.Embed(title=f"Ship name: {name1}{name2}", description=None, colour=0xb18dff)
            embed.add_field(name="Compatibility.", value=f"{ship_value}% [#######---] Good match.")
        elif ship_value >= 60:
            embed = discord.Embed(title=f"Ship name: {name1}{name2}", description=None, colour=0xb18dff)
            embed.add_field(name="Compatibility.", value=f"{ship_value}% [######----] Okay match.")
        elif ship_value >= 50:
            embed = discord.Embed(title=f"Ship name: {name1}{name2}", description=None, colour=0xb18dff)
            embed.add_field(name="Compatibility.", value=f"{ship_value}% [#####-----] Okay match.")
        elif ship_value >= 40:
            embed = discord.Embed(title=f"Ship name: {name1}{name2}", description=None, colour=0xb18dff)
            embed.add_field(name="Compatibility.", value=f"{ship_value}% [####------] Barely a thing.")
        elif ship_value >= 30:
            embed = discord.Embed(title=f"Ship name: {name1}{name2}", description=None, colour=0xb18dff)
            embed.add_field(name="Compatibility.", value=f"{ship_value}% [###-------] Barely a thing.")
        elif ship_value >= 20:
            embed = discord.Embed(title=f"Ship name: {name1}{name2}", description=None, colour=0xb18dff)
            embed.add_field(name="Compatibility.", value=f"{ship_value}% [##--------] Don't even try.")
        elif ship_value >= 10:
            embed = discord.Embed(title=f"Ship name: {name1}{name2}", description=None, colour=0xb18dff)
            embed.add_field(name="Compatibility.", value=f"{ship_value}% [#---------] This is awful.")
        elif ship_value >= 10:
            embed = discord.Embed(title=f"Ship name: {name1}{name2}", description=None, colour=0xb18dff)
            embed.add_field(name="Compatibility.", value=f"{ship_value}% [#---------] Just stop.")
        else:
            embed = discord.Embed(title=f"Ship name: {name1}{name2}", description=None, colour=0xb18dff)
            embed.add_field(name="Compatibility.", value=f"{ship_value}% [----------] No.")

        await ctx.send(f"💜`{arg1}`\n💜`{arg2}`")
        await ctx.send(embed=embed)

    @commands.command(name="8ball",
                      aliases=["eightball", "8", "ball"],
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


def setup(bot):
    bot.add_cog(Fun(bot.moose))
