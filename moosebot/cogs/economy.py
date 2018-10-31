import asyncio
import datetime
import random

import discord
from discord.ext import commands

from moosebot import MooseBot, converters


class Economy:

    def __init__(self, bot: MooseBot):
        self.bot = bot
        self.db = self.bot.database.db

    async def on_message(self, message):
        if message.guild is None:
            return
        elif message.author.bot:
            return
        else:
            await asyncio.gather(self.pickchance(message))

    async def pickchance(self, message):
        chance = random.randint(1, 1000)
        amount = random.randint(50, 250)
        if chance < 25 and message.content.lower() != 'dab':
            gen_message = await message.channel.send(
                f"`{amount}Ᵽ` has spawned! Type `dab` to collect it! You have 60 seconds")

            def check(m):
                return m.content.lower() == 'dab' and m.channel == message.channel

            try:
                msg = await self.bot.client.wait_for('message', check=check, timeout=60)
                try:
                    if 'Dab Multiplier' not in \
                            (await self.db.money.find_one({'userid': str(message.author.id)}))['inventory']:
                        grant = f"{msg.author.mention} dabbed on the Ᵽlaceholders. `{amount}Ᵽ` awarded to them."
                        await self.db.money.update_one({'userid': str(msg.author.id)}, {'$inc': {'balance': amount}}, True)
                    elif 'Dab Multiplier' in \
                        (await self.db.money.find_one({'userid': str(message.author.id)}))['inventory']:

                        grant = f"{msg.author.mention} dabbed on the Ᵽlaceholders." \
                                f"They had a Dab Multiplier so they got double Ᵽ." \
                                f"`{amount * 2}Ᵽ` awarded to them."

                        await self.db.money.update_one({'userid': str(msg.author.id)}, {'$inc': {'balance': amount * 2}},
                                                   True)
                except KeyError:
                    grant = f"{msg.author.mention} dabbed on the Ᵽlaceholders. `{amount}Ᵽ` awarded to them."
                    await self.db.money.update_one({'userid': str(msg.author.id)}, {'$inc': {'balance': amount}}, True)
                except TypeError:
                    grant = f"{msg.author.mention} dabbed on the Ᵽlaceholders. `{amount}Ᵽ` awarded to them."
                    await self.db.money.update_one({'userid': str(msg.author.id)}, {'$inc': {'balance': amount}}, True)
                await message.channel.send(grant)
                await gen_message.edit(
                    content=f"~~`{amount}Ᵽ` has spawned! Type `dab` to collect it! You have 60 seconds~~")

            except asyncio.TimeoutError:
                await message.channel.send("You took to long to dab the Ᵽ.")
                await gen_message.edit(
                    content=f"~~`{amount}Ᵽ` has spawned! Type `dab` to collect it! You have 60 seconds~~")

    @commands.command(aliases=['bal'], help='Check your balance.')
    async def balance(self, ctx, user: converters.FullMember = None):
        user = user or ctx.author
        if user is not None:
            if isinstance(user, discord.Member):
                try:
                    self.bot.client.get_user(user.id)
                    balance = await self.db.money.find_one({'userid': str(user.id)})
                    user = user.display_name
                except AttributeError:
                    user = user.id
            else:
                await ctx.send("That's not a person...")
                return

        else:
            balance = await self.db.money.find_one({'userid': str(ctx.author.id)})

        if balance is None:
            await ctx.send(f'{user} is broke and has 0Ᵽ.')
        else:
            embed = discord.Embed(title=f"{user}'s Ᵽlaceholders.", description=f'{balance["balance"]}Ᵽ',
                                  colour=0xb18dff)
            await ctx.send(embed=embed)

    @commands.command(aliases=['award'], help='Bot author only command.')
    @commands.check(MooseBot.is_owner)
    async def givep(self, ctx, amount: int, *, user: converters.FullMember):
        user = user or None
        amount = amount or None
        if user is None or not isinstance(user, discord.Member):
            await ctx.send("Please tell me who to give the Ᵽlaceholders to.")
        elif amount is None:
            await ctx.send("Please tell me how many Ᵽlaceholders to give.")
        else:
            try:
                amount = int(amount)
                await self.db.money.update_one({'userid': str(user.id)}, {'$inc': {'balance': amount}}, True)
                await ctx.send(f'`{amount}Ᵽ` was given to `{user.display_name}`')
            except Exception:
                await ctx.send("The amount to give the person needs to be a number.")

    @commands.command(help='Bot author only command.')
    @commands.check(MooseBot.is_owner)
    async def takep(self, ctx, amount=None, *, user: converters.FullMember = None):
        user = user or None
        amount = amount or None
        if user is None or not isinstance(user, discord.Member):
            await ctx.send("Please tell me who to take the Ᵽlaceholders from.")
        elif amount is None:
            await ctx.send("Please tell me how many Ᵽlaceholders to take.")
        else:
            try:
                amount = int(amount)

                if await self.db.money.find_one({'userid': str(user.id)})['balance'] is None or \
                        self.db.money.find_one({'userid': str(user.id)})['balance'] == 0:
                    await ctx.send(f"`{user.display_name} is already poor enough, no more can be taken from them.")
                elif await self.db.money.find_one({'userid': str(user.id)})['balance'] - amount < 0:
                    await ctx.send(
                        f"Doing this would cause `{user.display_name}` to go in to debt. Instead, we just set them to 0Ᵽ.")

                    await self.db.money.update_one({'userid': str(user.id)}, {'$inc': {'balance': 0}}, True)
                else:
                    await self.db.money.update_one({'userid': str(user.id)}, {'$inc': {'balance': -amount}}, True)
                    await ctx.send(f'`{amount}Ᵽ` was taken from `{user.display_name}`')

            except ValueError:
                await ctx.send("It needs to be `>takep amount user`")

    @commands.command(aliases=['give'], help='Pay another user some Ᵽlaceholders. \n`>pay amount user`')
    async def pay(self, ctx, amount=None, *, user: converters.FullMember = None):
        user = user or None
        amount = amount or None
        if user is None or not isinstance(user, discord.Member):
            await ctx.send("Use the command like this `>pay amount user`")
        elif amount is None:
            await ctx.send("Use the command like this `>pay amount user`")
        else:
            if amount == 'all':
                amount = await self.db.money.find_one({'userid': str(ctx.author.id)})['balance']
            try:
                amount = int(amount)
                if await self.db.money.find_one({'userid': str(ctx.author.id)})['balance'] is None or await \
                        self.db.money.find_one({'userid': str(ctx.author.id)})['balance'] < amount:
                    await ctx.send("You do not have enough Ᵽlaceholders to give that amount.")
                elif amount <= 0:
                    await ctx.send("You need to give an amount more than 0.")
                else:
                    await self.db.money.update_one({'userid': str(ctx.author.id)}, {'$inc': {'balance': -amount}})
                    await self.db.money.update_one({'userid': str(user.id)}, {'$inc': {'balance': amount}}, True)
                    await ctx.send(f"You have paid `{user.display_name}` {amount}Ᵽ")

            except ValueError:
                await ctx.send("The amount to pay needs to be a number.")

    @commands.command()
    async def daily(self, ctx):
        user = str(ctx.author.id)
        try:
            person = await self.db.money.find_one({'userid': user})['daily']
            if person is None:
                await self.db.money.update_one({'userid': user}, {'$inc': {'balance': 500}}, True)
                await self.db.money.update_one({'userid': user}, {'$set': {'daily': datetime.datetime.today()}})
                await ctx.send('500Ᵽ awarded for daily!')
            elif await self.db.money.find_one({'userid': user})['daily'] + datetime.timedelta(
                    days=1) < datetime.datetime.today():
                await self.db.money.update_one({'userid': user}, {'$inc': {'balance': 500}}, True)
                await self.db.money.update_one({'userid': user}, {'$set': {'daily': datetime.datetime.today()}})
                await ctx.send('500Ᵽ awarded for daily!')
            else:
                time = await self.db.money.find_one({'userid': user})['daily']
                timeleft = (await self.db.money.find_one({'userid': user})['daily'] + datetime.timedelta(
                    days=1)) - datetime.datetime.today()
                seconds = timeleft.total_seconds()
                minutes = int((seconds % 3600) // 60)
                hours = int(seconds // 3600)
                await ctx.send(
                    f"You've already claimed your daily for today. Come back in {f'{hours} hours, ' if hours != 0 else ''}{minutes} minutes and {int(seconds % 60)} seconds.")
        except Exception:
            await self.db.money.update_one({'userid': user}, {'$inc': {'balance': 500}}, True)
            await self.db.money.update_one({'userid': user}, {'$set': {'daily': datetime.datetime.today()}})
            await ctx.send('500Ᵽ awarded for daily!')

    @commands.command()
    async def weekly(self, ctx):
        user = str(ctx.author.id)
        try:
            person = await self.db.money.find_one({'userid': user})['weekly']
            if person is None:
                await self.db.money.update_one({'userid': user}, {'$inc': {'balance': 2500}}, True)
                await self.db.money.update_one({'userid': user}, {'$set': {'weekly': datetime.datetime.today()}})
                await ctx.send('2500Ᵽ awarded for weekly!')
            elif await self.db.money.find_one({'userid': user})['weekly'] + datetime.timedelta(
                    days=7) < datetime.datetime.today():
                await self.db.money.update_one({'userid': user}, {'$inc': {'balance': 2500}}, True)
                await self.db.money.update_one({'userid': user}, {'$set': {'weekly': datetime.datetime.today()}})
                await ctx.send('2500Ᵽ awarded for weekly!')
            else:
                time = await self.db.money.find_one({'userid': user})['weekly']
                timeleft = (await self.db.money.find_one({'userid': user})['weekly'] + datetime.timedelta(
                    days=7)) - datetime.datetime.today()
                seconds = timeleft.total_seconds()
                minutes = int((seconds % 3600) // 60)
                hours = int(seconds % 86400) // 3600
                days = int(seconds // 86400)
                await ctx.send(
                    f"You've already claimed your weekly for this week. Come back in {f'{days} days, ' if days != 0 else ''}{f'{hours} hours, ' if hours != 0 else ''}{minutes} minutes and {int(seconds % 60)} seconds.")
        except Exception:
            await self.db.money.update_one({'userid': user}, {'$inc': {'balance': 2500}}, True)
            await self.db.money.update_one({'userid': user}, {'$set': {'weekly': datetime.datetime.today()}})
            await ctx.send('2500Ᵽ awarded for weekly!')

    @commands.command(aliases=['baltop', 'richlist', 'ballb'], help='See the list of the richest people.')
    async def balancelb(self, ctx):
        order = 1
        people = {}
        async for i in self.db.money.find():
            try:
                user = self.bot.client.get_user(int(i['userid']))
                if i['balance'] == 0:
                    continue
                else:
                    people[user.display_name] = i["balance"]
            except Exception:
                continue
        people = sorted(people.items(), key=lambda kv: kv[1], reverse=True)
        eligable = []
        for i in people:
            eligable.append(f'▫{order}. **{i[0]}**: {i[1]}Ᵽ\n')
            order += 1

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
                reaction, user = await self.bot.client.wait_for('reaction_add', timeout=10, check=check)
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
                        embed = discord.Embed(title="Balance Leaderboard.", description=''.join(pages[curpage - 1]),
                                              colour=0xb18dff)
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
                        embed = discord.Embed(title="Balance Leaderboard.", description=''.join(pages[curpage + 1]),
                                              colour=0xb18dff)
                        embed.set_footer(text=f'Page ({foot_page}/{pagesamount+1})')
                        await msg.edit(embed=embed)
                        curpage += 1
                    await msg.remove_reaction(emoji='▶', member=ctx.author)

    @commands.command()
    async def wheel(self, ctx, amount=None):
        user = str(ctx.author.id)
        chance = random.randint(1, 8)
        amount = amount or None
        if amount is None:
            amount = 2
        elif amount == 'all':
            amount = int(await self.db.money.find_one({'userid': user})['balance'])
        try:
            amount = int(amount)
            if int(amount) <= 0:
                await ctx.send('You need to bet at least 1Ᵽ.')
            elif await self.db.money.find_one({'userid': user})['balance'] is None or await \
                    self.db.money.find_one({'userid': user})['balance'] < int(amount):
                await ctx.send('You do not have enough Ᵽ to bet that amount.')
                await self.db.money.update_one({'userid': user}, {'$inc': {'balance': -amount}})
            if chance == 1:
                embed = discord.Embed(title=f'**{ctx.author} has won: {int(amount * 1.5)}Ᵽ**',
                                      description='**『1.5』 『1.7』 『2.4』\n\n『0.2』   ↖   『1.2』\n\n『0.1』 『0.3』 『0.5』**',
                                      colour=0xb18dff)
                await ctx.send(embed=embed)
                win = int(amount * 1.5)
            elif chance == 2:
                embed = discord.Embed(title=f'**{ctx.author} has won: {int(amount * 1.7)}Ᵽ**',
                                      description='**『1.5』 『1.7』 『2.4』\n\n『0.2』   ⬆   『1.2』\n\n『0.1』 『0.3』 『0.5』**',
                                      colour=0xb18dff)
                await ctx.send(embed=embed)
                win = int(amount * 1.7)
            elif chance == 3:
                embed = discord.Embed(title=f'**{ctx.author} has won: {int(amount * 2.4)}Ᵽ**',
                                      description='**『1.5』 『1.7』 『2.4』\n\n『0.2』   ↗   『1.2』\n\n『0.1』 『0.3』 『0.5』**',
                                      colour=0xb18dff)
                await ctx.send(embed=embed)
                win = int(amount * 2.4)
            elif chance == 4:
                embed = discord.Embed(title=f'**{ctx.author} has won: {int(amount * 0.2)}Ᵽ**',
                                      description='**『1.5』 『1.7』 『2.4』\n\n『0.2』   ⬅   『1.2』\n\n『0.1』 『0.3』 『0.5』**',
                                      colour=0xb18dff)
                await ctx.send(embed=embed)
                win = int(amount * 0.2)
            elif chance == 5:
                embed = discord.Embed(title=f'**{ctx.author} has won: {int(amount * 1.2)}Ᵽ**',
                                      description='**『1.5』 『1.7』 『2.4』\n\n『0.2』   ➡   『1.2』\n\n『0.1』 『0.3』 『0.5』**',
                                      colour=0xb18dff)
                await ctx.send(embed=embed)
                win = int(amount * 1.2)
            elif chance == 6:
                embed = discord.Embed(title=f'**{ctx.author} has won: {int(amount * 0.1)}Ᵽ**',
                                      description='**『1.5』 『1.7』 『2.4』\n\n『0.2』   ↙   『1.2』\n\n『0.1』 『0.3』 『0.5』**',
                                      colour=0xb18dff)
                await ctx.send(embed=embed)
                win = int(amount * 0.1)
            elif chance == 7:
                embed = discord.Embed(title=f'**{ctx.author} has won: {int(amount * 0.3)}Ᵽ**',
                                      description='**『1.5』 『1.7』 『2.4』\n\n『0.2』   ⬇   『1.2』\n\n『0.1』 『0.3』 『0.5』**',
                                      colour=0xb18dff)
                await ctx.send(embed=embed)
                win = int(amount * 0.3)
            elif chance == 8:
                embed = discord.Embed(title=f'**{ctx.author} has won: {int(amount * 0.5)}Ᵽ**',
                                      description='**『1.5』 『1.7』 『2.4』\n\n『0.2』   ↘   『1.2』\n\n『0.1』 『0.3』 『0.5』**',
                                      colour=0xb18dff)
                await ctx.send(embed=embed)
                win = int(amount * 0.5)
            await self.db.money.update_one({'userid': user}, {'$inc': {'balance': win}})

        except ValueError:
            await ctx.send('You need to bet an amount... Not whatever that was...')

    @commands.command(aliases=['br'])
    async def betroll(self, ctx, amount=None):
        user = str(ctx.author.id)
        chance = random.randint(1, 100)
        amount = amount or None
        if amount is None:
            amount = 1
        elif amount == 'all':
            amount = int(await self.db.money.find_one({'userid': user})['balance'])
        try:
            amount = int(amount)
            if amount <= 0:
                await ctx.send('You need to bet at least 1Ᵽ.')
            elif await self.db.money.find_one({'userid': user})['balance'] is None or await \
                    self.db.money.find_one({'userid': user})['balance'] < amount:
                await ctx.send('You do not have enough Ᵽ to bet that amount.')
            await self.db.money.update_one({'userid': user}, {'$inc': {'balance': -amount}})
            if chance == 100:
                await ctx.send(f'You rolled `100` and won `{amount*10}Ᵽ` for rolling 100.')
                win = amount * 10
                await self.db.money.update_one({'userid': user}, {'$inc': {'balance': win}})
            elif chance >= 90:
                await ctx.send(f'You rolled `{chance}` and won `{amount*4}Ᵽ` for rolling 90+.')
                win = amount * 4
                await self.db.money.update_one({'userid': user}, {'$inc': {'balance': win}})
            elif chance >= 66:
                await ctx.send(f'You rolled `{chance}` and won `{amount*2}Ᵽ` for rolling 66+.')
                win = amount * 2
                await self.db.money.update_one({'userid': user}, {'$inc': {'balance': win}})
            else:
                await ctx.send(f'You rolled `{chance}`. Better luck next time...')
        except ValueError:
            await ctx.send('You need to bet a number... Not whatever that was.')

    @commands.command(aliases=['cf', 'bf', 'betflip'],
                      help='Flip a coin and bet heads or tails. Win to double up. \n`>cf amount side`')
    async def coinflip(self, ctx, amount=None, side=None):
        side = side or None
        user = str(ctx.author.id)
        amount = amount or None
        if amount is None:
            amount = 1
        elif amount == 'all':
            amount = int(await self.db.money.find_one({'userid': user})['balance'])
        sides = ['t', 'h', 'tail', 'head']
        choices = ['heads', 'tails']

        if side is None or side.lower() not in sides:
            await ctx.send('Please use the command like this `>coinflip amount side`.')
        else:
            if side.lower() == 'h':
                side = 'heads'
            elif side.lower() == 't':
                side = 'tails'
            try:
                amount = int(amount)
                if amount <= 0:
                    await ctx.send('You need to bet at least 1Ᵽ.')
                elif await self.db.money.find_one({'userid': user})['balance'] is None or await \
                        self.db.money.find_one({'userid': user})['balance'] < amount:
                    await ctx.send('You do not have enough Ᵽ to bet that amount.')
                else:
                    await self.db.money.update_one({'userid': str(user)}, {'$inc': {'balance': -amount}})
                    flipside = random.choice(choices)
                    if flipside == side.lower():
                        await ctx.send(f"I flipped {flipside.title()}, you win `{amount}Ᵽ`")
                        await self.db.money.update_one({'userid': str(user)}, {'$inc': {'balance': amount * 2}})
                    else:
                        await ctx.send(f"I flipped {flipside.title()}, you lose. Sorry.")
            except Exception:
                if amount.lower() == 'all':
                    amount = await self.db.money.find_one({'userid': user})['balance']
                    flipside = random.choice(choices)
                    await self.db.money.update_one({'userid': str(user)}, {'$inc': {'balance': 0}})
                    if flipside == side.lower():
                        await ctx.send(f"I flipped {flipside.title()}, you win `{amount}Ᵽ`")
                        await self.db.money.update_one({'userid': str(user)}, {'$inc': {'balance': amount * 2}})
                    else:
                        await ctx.send(f"I flipped {flipside.title()}, you lose. Sorry.")
                else:
                    await ctx.send("You need to give me a number to gamble. Not whatever that was...")

    async def get_input(self, ctx, datatype, error=''):
        while True:
            try:
                message = await self.bot.client.wait_for('message', check=lambda message: message.author is ctx.author,
                                                         timeout=60)
                datatype(message.content)
                return message.content
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

    @commands.command()
    async def work(self, ctx, game=None):
        game = game or None
        user = str(ctx.author.id)
        binary = ['b', 'bin', 'binary']

        if game is None:
            await ctx.send('Please specify the type of work you want to do. (Binary/more to come)')

        elif game.lower() in binary:

            async def play():
                choice = random.randint(1, 255)
                await ctx.send(f'What is `{choice}` in binary?')
                answer = await self.get_input(ctx, int, 'Enter a number, not that...')
                if int(answer) == int(f'{choice:b}'):
                    award = random.randint(20, 70)
                    await ctx.send(
                        f"Well done! That's correct, `{choice}` in binary is `{choice:b}`. You won `{award}Ᵽ`")
                    await self.db.money.update_one({'userid': user}, {'$inc': {'balance': award}}, True)
                    await self.gameover(ctx, play)
                else:
                    try:
                        wrong = int(answer, 2)
                    except ValueError:
                        wrong = int(answer)
                    await ctx.send(f"That was incorrect. `{choice}` in binary is `{choice:b}`. You entered `{wrong}`")
                    await self.gameover(ctx, play)

            await play()
