import asyncio
import datetime
import random
from threading import Lock

import discord
import pymongo
from discord.ext import commands
from discord.ext.commands import Cog

from moosebot import MooseBot, converters


class Economy(Cog):

    def __init__(self, bot: MooseBot):
        self.lock = Lock()
        self.bot = bot
        self.db = self.bot.database.db

    @Cog.listener()
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
        if message.channel.topic is not None and message.channel.topic.startswith(">count"):
            return
        else:
            if chance < 10 and message.content.lower() != 'dab':
                gen_message = await message.channel.send(
                    f"`{amount}{MooseBot.currency}` has spawned! Type `dab` to collect it! You have 60 seconds")

                def check(m):
                    return m.content.lower() == 'dab'or m.content.lower() == 'даб' and m.channel == message.channel

                try:
                    msg = await self.bot.client.wait_for('message', check=check, timeout=60)
                    try:
                        person = await self.db.money.find_one({'userid': str(msg.author.id)})
                        if 'inventory' not in person:
                            grant = f"{msg.author.mention} dabbed on the {MooseBot.currency}. `{amount}{MooseBot.currency}` awarded to them."
                            await self.db.money.update_one({'userid': str(msg.author.id)}, {'$inc': {'balance': amount}}, True)
                            grantmsg = await message.channel.send(grant)
                            # await gen_message.edit(content=f"~~`{amount}{MooseBot.currency}` has spawned! Type `dab` to collect it! You have 60 seconds~~")
                            await gen_message.delete()
                            await msg.delete()
                            await asyncio.sleep(3)
                            await grantmsg.delete()
                            return
                        else:
                            inventory = person['inventory']
                            if 'Dab Multiplier' not in inventory:
                                grant = f"{msg.author.mention} dabbed on the {MooseBot.currency}. `{amount}{MooseBot.currency}` awarded to them."
                                await self.db.money.update_one({'userid': str(msg.author.id)}, {'$inc': {'balance': amount}}, True)
                            elif 'Dab Multiplier' in inventory:

                                grant = f"{msg.author.mention} dabbed on the {MooseBot.currency}. " \
                                        f"They had a Dab Multiplier so they got double {MooseBot.currency}. " \
                                        f"`{amount * 2}{MooseBot.currency}` awarded to them."

                                await self.db.money.update_one({'userid': str(msg.author.id)}, {'$inc': {'balance': amount * 2}},
                                                           True)

                    except KeyError:
                        grant = f"{msg.author.mention} dabbed on the {MooseBot.currency}. `{amount}{MooseBot.currency}` awarded to them."
                        await self.db.money.update_one({'userid': str(msg.author.id)}, {'$inc': {'balance': amount}}, True)
                    except TypeError:
                        grant = f"{msg.author.mention} dabbed on the {MooseBot.currency}. `{amount}{MooseBot.currency}` awarded to them."
                        await self.db.money.update_one({'userid': str(msg.author.id)}, {'$inc': {'balance': amount}}, True)
                    grantmsg = await message.channel.send(grant)
                    # await gen_message.edit(content=f"~~`{amount}{MooseBot.currency}` has spawned! Type `dab` to collect it! You have 60 seconds~~")
                    await gen_message.delete()
                    await msg.delete()
                    await asyncio.sleep(3)
                    await grantmsg.delete()

                except asyncio.TimeoutError:
                    toolate = await message.channel.send(f"You took to long to dab the {MooseBot.currency}.")
                    # await gen_message.edit(content=f"~~`{amount}{MooseBot.currency}` has spawned! Type `dab` to collect it! You have 60 seconds~~")
                    await gen_message.delete()
                    await asyncio.sleep(5)
                    await toolate.delete()

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
            await ctx.send(f'{user} is broke and has 0{MooseBot.currency}.')
        else:
            embed = discord.Embed(title=f"{user}'s {MooseBot.currency}.", description=f'{balance["balance"]}{MooseBot.currency}',
                                  colour=0xb18dff)
            await ctx.send(embed=embed)

    @commands.command(aliases=['award'], help='Bot author only command.', hidden=True)
    @commands.check(MooseBot.is_owner)
    async def givep(self, ctx, amount: int, *, user: converters.FullMember):
        user = user or None
        amount = amount or None
        if user is None or not isinstance(user, discord.Member):
            await ctx.send(f"Please tell me who to give the {MooseBot.currency} to.")
        elif amount is None:
            await ctx.send(f"Please tell me how many {MooseBot.currency} to give.")
        else:
            try:
                amount = int(amount)
                await self.db.money.update_one({'userid': str(user.id)}, {'$inc': {'balance': amount}}, True)
                await ctx.send(f'`{amount}{MooseBot.currency}` was given to `{user.display_name}`')
            except Exception:
                await ctx.send("The amount to give the person needs to be a number.")

    @commands.command(help='Bot author only command.', hidden=True)
    @commands.check(MooseBot.is_owner)
    async def takep(self, ctx, amount=None, *, user: converters.FullMember = None):
        user = user or None
        amount = amount or None
        if user is None or not isinstance(user, discord.Member):
            await ctx.send(f"Please tell me who to take the {MooseBot.currency} from.")
        elif amount is None:
            await ctx.send(f"Please tell me how many {MooseBot.currency} to take.")
        else:
            try:
                amount = int(amount)

                if (await self.db.money.find_one({'userid': str(user.id)}))['balance'] is None or (await self.db.money.find_one({'userid': str(user.id)}))['balance'] == 0:
                    await ctx.send(f"{user.display_name} is already poor enough, no more can be taken from them.")
                elif (await self.db.money.find_one({'userid': str(user.id)}))['balance'] - amount < 0:
                    await ctx.send(
                        f"Doing this would cause `{user.display_name}` to go in to debt. Instead, we just set them to 0{MooseBot.currency}.")

                    await self.db.money.update_one({'userid': str(user.id)}, {'$inc': {'balance': 0}}, True)
                else:
                    await self.db.money.update_one({'userid': str(user.id)}, {'$inc': {'balance': -amount}}, True)
                    await ctx.send(f'`{amount}{MooseBot.currency}` was taken from `{user.display_name}`')

            except ValueError:
                await ctx.send("It needs to be `>takep amount user`")

    @commands.command(aliases=['give'], help=f'Pay another user some {MooseBot.currency}. \n`>pay amount user`')
    async def pay(self, ctx, amount=None, *, user: converters.FullMember = None):
        user = user or None
        amount = amount or None
        if user is None or not isinstance(user, discord.Member):
            await ctx.send("Use the command like this `>pay amount user`")
        elif amount is None:
            await ctx.send("Use the command like this `>pay amount user`")
        else:
            if amount == 'all':
                amount = (await self.db.money.find_one({'userid': str(ctx.author.id)}))['balance']
            try:
                amount = int(amount)
                if (await self.db.money.find_one({'userid': str(ctx.author.id)}))['balance'] is None or \
                        (await self.db.money.find_one({'userid': str(ctx.author.id)}))['balance'] < amount:
                    await ctx.send(f"You do not have enough {MooseBot.currency} to give that amount.")
                elif amount <= 0:
                    await ctx.send("You need to give an amount more than 0.")
                else:
                    await self.db.money.update_one({'userid': str(ctx.author.id)}, {'$inc': {'balance': -amount}})
                    await self.db.money.update_one({'userid': str(user.id)}, {'$inc': {'balance': amount}}, True)
                    await ctx.send(f"You have paid `{user.display_name}` {amount}{MooseBot.currency}")

            except ValueError:
                await ctx.send("The amount to pay needs to be a number.")

    @commands.command()
    async def daily(self, ctx):
        user = str(ctx.author.id)
        try:
            person = (await self.db.money.find_one({'userid': user}))['daily']
            if person is None:
                await self.db.money.update_one({'userid': user}, {'$inc': {'balance': 500}}, True)
                await self.db.money.update_one({'userid': user}, {'$set': {'daily': datetime.datetime.today()}})
                await ctx.send(f'500{MooseBot.currency} awarded for daily!')
            elif (await self.db.money.find_one({'userid': user}))['daily'] + datetime.timedelta(
                    days=1) < datetime.datetime.today():
                await self.db.money.update_one({'userid': user}, {'$inc': {'balance': 500}}, True)
                await self.db.money.update_one({'userid': user}, {'$set': {'daily': datetime.datetime.today()}})
                await ctx.send(f'500{MooseBot.currency} awarded for daily!')
            else:
                time = (await self.db.money.find_one({'userid': user}))['daily']
                timeleft = ((await self.db.money.find_one({'userid': user}))['daily'] + datetime.timedelta(
                    days=1)) - datetime.datetime.today()
                seconds = timeleft.total_seconds()
                minutes = int((seconds % 3600) // 60)
                hours = int(seconds // 3600)
                await ctx.send(
                    f"You've already claimed your daily for today. Come back in {f'{hours} hours, ' if hours != 0 else ''}{minutes} minutes and {int(seconds % 60)} seconds.")
        except Exception:
            await self.db.money.update_one({'userid': user}, {'$inc': {'balance': 500}}, True)
            await self.db.money.update_one({'userid': user}, {'$set': {'daily': datetime.datetime.today()}})
            await ctx.send(f'500{MooseBot.currency} awarded for daily!')

    @commands.command()
    async def weekly(self, ctx):
        user = str(ctx.author.id)
        try:
            person = (await self.db.money.find_one({'userid': user}))['weekly']
            if person is None:
                await self.db.money.update_one({'userid': user}, {'$inc': {'balance': 2500}}, True)
                await self.db.money.update_one({'userid': user}, {'$set': {'weekly': datetime.datetime.today()}})
                await ctx.send(f'2500{MooseBot.currency} awarded for weekly!')
            elif (await self.db.money.find_one({'userid': user}))['weekly'] + datetime.timedelta(
                    days=7) < datetime.datetime.today():
                await self.db.money.update_one({'userid': user}, {'$inc': {'balance': 2500}}, True)
                await self.db.money.update_one({'userid': user}, {'$set': {'weekly': datetime.datetime.today()}})
                await ctx.send(f'2500{MooseBot.currency} awarded for weekly!')
            else:
                time = (await self.db.money.find_one({'userid': user}))['weekly']
                timeleft = ((await self.db.money.find_one({'userid': user}))['weekly'] + datetime.timedelta(
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
            await ctx.send(f'2500{MooseBot.currency} awarded for weekly!')

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
            eligable.append(f'▫{order}. **{i[0]}**: {i[1]}{MooseBot.currency}\n')
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
        elif not isinstance(amount, int) and amount.lower() == 'all':
            amount = int((await self.db.money.find_one({'userid': user}))['balance'])
        elif not isinstance(amount, int) and amount.lower() == 'half':
            amount = (int((await self.db.money.find_one({'userid': user}))['balance']) / 2)
        try:
            amount = int(amount)
            if int(amount) <= 0:
                await ctx.send(f'You need to bet at least 1{MooseBot.currency}.')
            elif (await self.db.money.find_one({'userid': user}))['balance'] is None or (await self.db.money.find_one({'userid': user}))['balance'] < int(amount):
                await ctx.send(f'You do not have enough {MooseBot.currency} to bet that amount.')
            else:
                await self.db.money.update_one({'userid': user}, {'$inc': {'balance': -amount}})
                if chance == 1:
                    embed = discord.Embed(title=f'**{ctx.author} has won: {int(amount * 1.5)}{MooseBot.currency}**',
                                          description='**『1.5』 『1.7』 『2.4』\n\n『0.2』   ↖   『1.2』\n\n『0.1』 『0.3』 『0.5』**',
                                          colour=0xb18dff)
                    await ctx.send(embed=embed)
                    win = int(amount * 1.5)
                elif chance == 2:
                    embed = discord.Embed(title=f'**{ctx.author} has won: {int(amount * 1.7)}{MooseBot.currency}**',
                                          description='**『1.5』 『1.7』 『2.4』\n\n『0.2』   ⬆   『1.2』\n\n『0.1』 『0.3』 『0.5』**',
                                          colour=0xb18dff)
                    await ctx.send(embed=embed)
                    win = int(amount * 1.7)
                elif chance == 3:
                    embed = discord.Embed(title=f'**{ctx.author} has won: {int(amount * 2.4)}{MooseBot.currency}**',
                                          description='**『1.5』 『1.7』 『2.4』\n\n『0.2』   ↗   『1.2』\n\n『0.1』 『0.3』 『0.5』**',
                                          colour=0xb18dff)
                    await ctx.send(embed=embed)
                    win = int(amount * 2.4)
                elif chance == 4:
                    embed = discord.Embed(title=f'**{ctx.author} has won: {int(amount * 0.2)}{MooseBot.currency}**',
                                          description='**『1.5』 『1.7』 『2.4』\n\n『0.2』   ⬅   『1.2』\n\n『0.1』 『0.3』 『0.5』**',
                                          colour=0xb18dff)
                    await ctx.send(embed=embed)
                    win = int(amount * 0.2)
                elif chance == 5:
                    embed = discord.Embed(title=f'**{ctx.author} has won: {int(amount * 1.2)}{MooseBot.currency}**',
                                          description='**『1.5』 『1.7』 『2.4』\n\n『0.2』   ➡   『1.2』\n\n『0.1』 『0.3』 『0.5』**',
                                          colour=0xb18dff)
                    await ctx.send(embed=embed)
                    win = int(amount * 1.2)
                elif chance == 6:
                    embed = discord.Embed(title=f'**{ctx.author} has won: {int(amount * 0.1)}{MooseBot.currency}**',
                                          description='**『1.5』 『1.7』 『2.4』\n\n『0.2』   ↙   『1.2』\n\n『0.1』 『0.3』 『0.5』**',
                                          colour=0xb18dff)
                    await ctx.send(embed=embed)
                    win = int(amount * 0.1)
                elif chance == 7:
                    embed = discord.Embed(title=f'**{ctx.author} has won: {int(amount * 0.3)}{MooseBot.currency}**',
                                          description='**『1.5』 『1.7』 『2.4』\n\n『0.2』   ⬇   『1.2』\n\n『0.1』 『0.3』 『0.5』**',
                                          colour=0xb18dff)
                    await ctx.send(embed=embed)
                    win = int(amount * 0.3)
                elif chance == 8:
                    embed = discord.Embed(title=f'**{ctx.author} has won: {int(amount * 0.5)}{MooseBot.currency}**',
                                          description='**『1.5』 『1.7』 『2.4』\n\n『0.2』   ↘   『1.2』\n\n『0.1』 『0.3』 『0.5』**',
                                          colour=0xb18dff)
                    await ctx.send(embed=embed)
                    win = int(amount * 0.5)
                await self.db.money.update_one({'userid': user}, {'$inc': {'balance': win}})

        except ValueError:
            await ctx.send('You need to bet an amount... Not whatever that was...')

    @commands.command(hidden=True)
    @commands.check(MooseBot.is_owner)
    async def generate(self, ctx):
        people = self.bot.database.db.money
        for i in self.bot.client.guilds:
            for x in i.members:
                userid = str(x.id)
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

    @commands.command(hidden=True)
    @commands.check(MooseBot.is_owner)
    async def gen1(self, ctx, user: converters.PartialMember = None):
        user = user or None
        if user is None:
            await ctx.send('Tell me who to generate for')
        else:
            userid = str(user.id)
        people = self.bot.database.db.money
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
        await ctx.send(f'Generated tables for {user.display_name}')

    @commands.command(hidden=True)
    @commands.check(MooseBot.is_owner)
    async def reset(self, ctx):
        people = self.bot.database.db.money
        personlist = people.find()
        personlist.sort('price', pymongo.ASCENDING)
        for i in await personlist.to_list(length=200):
            person = await people.find_one({'userid': str(i['userid'])})
            print(person)
            # personlist = person.to_list(length=100)
            print(personlist)
            try:
                for x in person['inventory']:
                    await people.update_one({'userid': str(i['userid'])}, {'$pull': {'inventory': x}})

                for x in person['fish']['trophies']:
                    await people.update_one({'userid': str(i['userid'])}, {'$pull': {'fish.trophies': x}})
            except Exception:
                continue

            await people.update_one({'userid': str(i['userid'])}, {'$set': {'fish.totalweight': 0}})
            await people.update_one({'userid': str(i['userid'])}, {'$set': {'fish.largestfish': 0}})
            await people.update_one({'userid': str(i['userid'])}, {'$set': {'fish.recentfish': 0}})
            await people.update_one({'userid': str(i['userid'])}, {'$set': {'fish.totalfish': 0}})
            await people.update_one({'userid': str(i['userid'])}, {'$set': {'fish.sincelastsell': 0}})
            await people.update_one({'userid': str(i['userid'])}, {'$set': {'fish.rod': 'None'}})
            await people.update_one({'userid': str(i['userid'])}, {'$set': {'fish.curbait': 'None'}})
            await people.update_one({'userid': str(i['userid'])}, {'$set': {'fish.bait.Bait': 0}})
            await people.update_one({'userid': str(i['userid'])}, {'$set': {'fish.bait.Large Bait': 0}})
            await people.update_one({'userid': str(i['userid'])}, {'$set': {'fish.bait.Game Bait': 0}})
            await people.update_one({'userid': str(i['userid'])}, {'$set': {'balance': 0}})
            await people.update_one({'userid': str(i['userid'])}, {'$set': {'daily': 'None'}})
            await people.update_one({'userid': str(i['userid'])}, {'$set': {'weekly': 'None'}})

    @commands.command(aliases=['br'])
    async def betroll(self, ctx, amount=None):
        user = str(ctx.author.id)
        chance = random.randint(1, 100)
        amount = amount or None
        if amount is None:
            amount = 1
        elif amount == 'all':
            amount = int((await self.db.money.find_one({'userid': user}))['balance'])
        try:
            amount = int(amount)
            if amount <= 0:
                await ctx.send(f'You need to bet at least 1{MooseBot.currency}.')
            elif (await self.db.money.find_one({'userid': user}))['balance'] is None or (await self.db.money.find_one({'userid': user}))['balance'] < amount:
                await ctx.send(f'You do not have enough {MooseBot.currency} to bet that amount.')
                return
            else:
                await self.db.money.update_one({'userid': user}, {'$inc': {'balance': -amount}})
                if chance == 100:
                    await ctx.send(f'You rolled `100` and won `{amount*10}{MooseBot.currency}` for rolling 100.')
                    win = amount * 10
                    await self.db.money.update_one({'userid': user}, {'$inc': {'balance': win}})
                elif chance >= 90:
                    await ctx.send(f'You rolled `{chance}` and won `{amount*4}{MooseBot.currency}` for rolling 90+.')
                    win = amount * 4
                    await self.db.money.update_one({'userid': user}, {'$inc': {'balance': win}})
                elif chance >= 66:
                    await ctx.send(f'You rolled `{chance}` and won `{amount*2}{MooseBot.currency}` for rolling 66+.')
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
            amount = int((await self.db.money.find_one({'userid': user}))['balance'])
        sides = ['t', 'h', 'tail', 'head', 'heads', 'tails']
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
                    await ctx.send(f'You need to bet at least 1{MooseBot.currency}.')
                elif (await self.db.money.find_one({'userid': user}))['balance'] is None or (await self.db.money.find_one({'userid': user}))['balance'] < amount:
                    await ctx.send(f'You do not have enough {MooseBot.currency} to bet that amount.')
                else:
                    await self.db.money.update_one({'userid': str(user)}, {'$inc': {'balance': -amount}})
                    flipside = random.choice(choices)
                    if flipside == side.lower():
                        await ctx.send(f"I flipped {flipside.title()}, you win `{amount}{MooseBot.currency}`")
                        await self.db.money.update_one({'userid': str(user)}, {'$inc': {'balance': amount * 2}})
                    else:
                        await ctx.send(f"I flipped {flipside.title()}, you lose. Sorry.")
            except Exception:
                if amount.lower() == 'all':
                    amount = (await self.db.money.find_one({'userid': user}))['balance']
                    flipside = random.choice(choices)
                    await self.db.money.update_one({'userid': str(user)}, {'$inc': {'balance': 0}})
                    if flipside == side.lower():
                        await ctx.send(f"I flipped {flipside.title()}, you win `{amount}{MooseBot.currency}`")
                        await self.db.money.update_one({'userid': str(user)}, {'$inc': {'balance': amount * 2}})
                    else:
                        await ctx.send(f"I flipped {flipside.title()}, you lose. Sorry.")
                else:
                    await ctx.send("You need to give me a number to gamble. Not whatever that was...")

    # async def get_input(self, ctx, datatype, error=''):
    #     while True:
    #         try:
    #             message = await self.bot.client.wait_for('message', check=lambda msg: msg.author is ctx.author,
    #                                                      timeout=60)
    #             datatype(message.content)
    #             return message.content
    #         except TimeoutError:
    #             await ctx.send("You took too long to answer.")
    #             return
    #         except Exception:
    #             await ctx.send(error)
    #
    # async def gameover(self, ctx, funct):
    #     await ctx.send("Do you want to play again? (**Yes**/**No**)")
    #     self.message = await self.get_input(ctx, str)
    #     self.message = self.message.lower()
    #
    #     if self.message == 'yes' or self.message == 'y':
    #         await funct()
    #     elif self.message == 'no' or self.message == 'n':
    #         await ctx.send("Thanks for playing!")
    #     else:
    #         await self.gameover(ctx, funct)
    #
    # @commands.command(hidden=True)
    # @commands.check(MooseBot.is_owner)
    # async def work(self, ctx, game=None):
    #     game = game or None
    #     user = str(ctx.author.id)
    #     binary = ['b', 'bin', 'binary']
    #
    #     if game is None:
    #         await ctx.send('Please specify the type of work you want to do. (Binary/more to come)')
    #
    #     elif game.lower() in binary:
    #
    #         async def play():
    #             choice = random.randint(1, 255)
    #             await ctx.send(f'What is `{choice}` in binary?')
    #             answer = await self.get_input(ctx, int, 'Enter a number, not that...')
    #             if int(answer) == int(f'{choice:b}'):
    #                 award = random.randint(20, 70)
    #                 await ctx.send(
    #                     f"Well done! That's correct, `{choice}` in binary is `{choice:b}`. You won `{award}{MooseBot.currency}`")
    #                 await self.db.money.update_one({'userid': user}, {'$inc': {'balance': award}}, True)
    #                 await self.gameover(ctx, play)
    #             else:
    #                 try:
    #                     wrong = int(answer, 2)
    #                 except ValueError:
    #                     wrong = int(answer)
    #                 await ctx.send(f"That was incorrect. `{choice}` in binary is `{choice:b}`. You entered `{wrong}`")
    #                 await self.gameover(ctx, play)
    #
    #         await play()

    @commands.command(hidden=True)
    @commands.check(MooseBot.is_owner)
    async def event(self, ctx, amount=None, time: int=None):
        amount = amount or None
        time = time or 300
        if time < 0:
            await ctx.send("You need to specify a time that is more than 0 seconds.")
            return
        if amount is None:
            await ctx.send("You need to specify an amount for the event.")
        else:
            list = [445936072288108544]
            seconds = int(time % 60)
            minutes = int((time % 3600) // 60)
            hours = int(time // 3600)
            embed = discord.Embed(title="Reaction event.", description=f"React with a 🐛 to be awarded `{amount}{MooseBot.currency}`", colour=0xb18dff)
            embed.set_footer(text=f"This event will run for{f' {hours} hours' if hours != 0 else ''}{f',' if hours != 0 and minutes != 0 else ''}{f' {minutes} minutes' if minutes != 0 else ''}{f' and' if minutes != 0 and seconds != 0 else ''}{f' {seconds} seconds' if seconds != 0 else ''} from when it was created.")
            msg = await ctx.send(embed=embed)
            await msg.add_reaction("🐛")
            await ctx.message.delete()
            while True:

                def check(reaction, user):
                    return user.id not in list and str(reaction.emoji) == '🐛'

                try:
                    reaction, user = await self.bot.client.wait_for('reaction_add', timeout=int(time), check=check)
                    list.append(user.id)
                    await self.db.money.update_one({'userid': str(user.id)}, {'$inc': {'balance': int(amount)}}, True)

                except asyncio.TimeoutError:
                    await msg.delete()
                    break


def setup(bot):
    bot.add_cog(Economy(bot.moose))
