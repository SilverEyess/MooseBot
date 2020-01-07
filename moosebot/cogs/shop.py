import asyncio

import discord
import pymongo
from discord.ext import commands
from discord.ext.commands import Cog

from moosebot import MooseBot, cog_group


@cog_group("Economy")
class Shop(Cog):

    def __init__(self, bot: MooseBot):
        self.bot = bot

    @commands.command()
    @commands.check(MooseBot.is_owner)
    async def additem(self, ctx, price=None, *, item=None, ):
        item = item or None
        price = price or None
        shop = self.bot.database.db.shop
        if item is None:
            await ctx.send("Tell me what item you want to add, and at what price. `>additem price item`")
        elif price is None:
            await ctx.send("Tell me what item you want to add, and at what price. `>additem price item`")
        else:
            try:
                price = int(price)
                if price < 0:
                    await ctx.send("You can't set the price for an item to be 0 or less.")
                else:
                    await shop.insert_one({'name': item, 'name_lower': item.lower(), 'price': price, 'limit': 1})
                    await ctx.send(f'{item} was added to the shop for {price}Ᵽ')
            except ValueError:
                await ctx.send("You need to specify a numerical price. Not whatever that was...")

    @commands.command()
    @commands.check(MooseBot.is_owner)
    async def removeitem(self, ctx, *, item):
        shop = self.bot.database.db.shop
        item = item or None
        if item is None:
            await ctx.send("You need to say what item you want to remove from the shop. `>removeitem item`")
        else:
            match = await shop.find_one({'name_lower': item.lower()})
            if match is None:
                await ctx.send(f'Could not find {item} in the shop.')
            else:
                await shop.delete_one({'name_lower': item.lower()})
                await ctx.send(f'{item.title()} has been removed from the shop.')

    @commands.command(aliases=['store'])
    async def shop(self, ctx):
        shop = self.bot.database.db.shop
        person = await self.bot.database.db.money.find_one({'userid': str(ctx.author.id)})
        pages = int((await shop.count_documents({})) / 9)
        if pages == 0:
            pages = 1
        pagelength = 0
        embed = discord.Embed(title='MooseBot Shop.', colour=0xb18dff)
        order = 0
        shoplist = shop.find()
        shoplist.sort('price', pymongo.ASCENDING)
        skip = 0

        for i in await shoplist.to_list(length=9):
            limit = i['limit']
            order += 1
            if 'inventory' in person:
                inventory = person['inventory']
                if i['name'] in inventory and limit == 1:
                    embed.add_field(name=f'#{order}: {i["name"]} ✅', value=f'{i["price"]:,d}Ᵽ')
                elif limit > 1:
                    if 'Bait Bucket' in inventory:
                        limit = limit * 3
                    if i['name'].lower().endswith('bait'):
                        if 'fish' in person:
                            fishtable = person['fish']
                            if 'bait' in fishtable:
                                baittable = fishtable['bait']
                                baittotal = 0
                                for x in baittable:
                                    baittotal += int(baittable[x])
                                embed.add_field(name=f'#{order}: {i["name"]} {baittotal}/{limit}', value=f'{i["price"]:,d}Ᵽ')
                            else:
                                embed.add_field(name=f'#{order}: {i["name"]} 0/{i["limit"]}', value=f'{i["price"]:,d}Ᵽ')
                        else:
                            embed.add_field(name=f'#{order}: {i["name"]} 0/{limit}', value=f'{i["price"]:,d}Ᵽ')
                else:
                    embed.add_field(name=f'#{order}: {i["name"]}', value=f'{i["price"]:,d}Ᵽ')
            else:
                embed.add_field(name=f'#{order}: {i["name"]}', value=f'{i["price"]:,d}Ᵽ')

            pagelength += 1
        curpage = 1
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
                if str(reaction.emoji) == '▶' and user == ctx.author:
                    if curpage == pages + 1:
                        await msg.remove_reaction(emoji='▶', member=ctx.author)
                        continue
                    else:
                        skip += 9
                        curpage += 1
                        embed.clear_fields()
                        shoplist = shop.find()
                        shoplist.sort('price', pymongo.ASCENDING).skip(skip)
                        for i in await shoplist.to_list(length=9):
                            order += 1
                            embed.add_field(name=f'#{order}: {i["name"]}', value=f'{i["price"]:,d}Ᵽ')
                            if curpage == pages:
                                pagelength += 1
                            else:
                                pagelength = 9

                        await msg.edit(embed=embed)
                        await msg.remove_reaction(emoji='▶', member=ctx.author)
                elif str(reaction.emoji) == '◀' and user == ctx.author:
                    if curpage == 1:
                        await msg.remove_reaction(emoji='◀', member=ctx.author)
                        continue
                    else:
                        skip -= 9
                        curpage -= 1
                        if curpage == 1:
                            order = 0
                        else:
                            order -= pagelength
                        embed.clear_fields()
                        shoplist = shop.find()
                        shoplist.sort('price', pymongo.ASCENDING).skip(skip)
                        for i in await shoplist.to_list(length=9):
                            order += 1
                            embed.add_field(name=f'#{order}: {i["name"]}', value=f'{i["price"]:,d}Ᵽ')
                            pagelength += 1
                        await msg.edit(embed=embed)
                    await msg.remove_reaction(emoji='◀', member=ctx.author)

    @commands.command()
    async def buy(self, ctx, amount, *, item=None):
        db = self.bot.database.db
        shop = db.shop
        user = str(ctx.author.id)
        item = item or None
        amount = amount or None
        if amount is None:
            await ctx.send("Please specify which item you want to buy and how many(optional), either by its name or number in the store. `>buy amount item`")
        else:
            try:
                amount = int(amount)
                if isinstance(amount, int):
                    if item is None:
                        item = amount
                        amount = 1
                    else:
                        amount = int(amount)
                        if amount <= 0:
                            await ctx.send("You need to purchase at least 1.")

            except Exception:
                item = amount
                # await ctx.send('idunno aye')
        if item is None:
            await ctx.send("Please specify which item you want to buy, either by its name or number in the store. `>buy item`")
        else:
            try:
                item = int(item)
                try:
                    shoplist = shop.find()
                    shoplist.sort('price', pymongo.ASCENDING).skip(item - 1)
                    for i in await shoplist.to_list(length=1):
                        item = i

                except Exception:
                    await ctx.send(f"There is no item #{item} on the store.")

            except ValueError:
                match = await shop.find_one({'name_lower': item.lower()})

                if match is None:
                    await ctx.send("That item does not exist on the store. For ease of use, use the item number.")

                else:
                    item = match

            # try:
            person = await db.money.find_one({'userid': user})
            if 'inventory' not in person:
                if amount is not None:
                    if person['balance'] < amount * item['price']:
                        await ctx.send("You do not have enough money to buy this.")
                    elif item['name'].endswith("Bait"):
                        await db.money.update_one({'userid': user}, {'$inc': {f'fish.bait.{item["name"]}': amount}})
                        await db.money.update_one({'userid': user}, {'$inc': {'balance': - (item['price'] * amount)}})
                        await ctx.send(f"Congratulations on your new purchase of {item['name']}! `{item['price'] * amount}Ᵽ` has been deducted from your account.")
                    else:
                        await db.money.update_one({'userid': user}, {'$push': {'inventory': item['name']}})
                        await db.money.update_one({'userid': user}, {'$inc': {'balance': - item['price']}})
                        await ctx.send(f"Congratulations on your new purchase of {item['name']}! `{item['price']}Ᵽ` has been deducted from your account.")

                elif person['balance'] < item['price']:
                    await ctx.send("You do not have enough money to buy this.")
                elif item['name'].endswith("Bait"):
                    await db.money.update_one({'userid': user}, {'$inc': {f'fish.bait.{item["name"]}': 1}})
                    await db.money.update_one({'userid': user}, {'$inc': {'balance': - item['price']}})
                    await ctx.send(f"Congratulations on your new purchase of {item['name']}! `{item['price']}Ᵽ` has been deducted from your account.")
                else:
                    await db.money.update_one({'userid': user}, {'$push': {'inventory': item['name']}})
                    await db.money.update_one({'userid': user}, {'$inc': {'balance': - item['price']}})
                    await ctx.send(f"Congratulations on your new purchase of {item['name']}! `{item['price']}Ᵽ` has been deducted from your account.")
            else:
                inventory = person['inventory']
                if item['name'].endswith("Bait"):
                    if 'Bait Bucket' in inventory:
                        buylimit = item['limit'] * 3
                    else:
                        buylimit = item['limit']
                    if 'fish' in person:
                        fishlist = person['fish']

                        if 'bait' in fishlist:
                            baitlist = fishlist['bait']
                            totalbait = 0
                            for x in baitlist:
                                totalbait += baitlist[x]
                        else:
                            if amount is not None:
                                if person['balance'] < amount * item['price']:
                                    await ctx.send('You need more money to buy that much.')
                                else:
                                    await db.money.update_one({'userid': user}, {'$inc': {f'fish.bait.{item["name"]}': amount}})
                                    await db.money.update_one({'userid': user}, {'$inc': {'balance': - (item['price'] * amount)}})
                                    await ctx.send(f"Congratulations on your new purchase of {amount} {item['name']}s! `{item['price'] * amount}Ᵽ` has been deducted from your account.")
                            else:
                                if person['balance'] < item['price']:
                                    await ctx.send('You need more money to buy this.')
                                else:
                                    await db.money.update_one({'userid': user}, {'$inc': {f'fish.bait.{item["name"]}': 1}})
                                    await db.money.update_one({'userid': user}, {'$inc': {'balance': - item['price']}})
                                    await ctx.send(f"Congratulations on your new purchase of {item['name']}! `{item['price']}Ᵽ` has been deducted from your account.")

                        if totalbait > buylimit:
                            await ctx.send("Looks like you've already got the maximum amount of bait. Do some fishing to exhaust it, or buy a bait bucket to hold more.")
                        elif amount + totalbait > buylimit:
                            await ctx.send("You can't hold that much bait bud, try a smaller amount.")
                        else:
                            if amount is not None:
                                if person['balance'] < amount * item['price']:
                                    await ctx.send('You need more money to buy that much.')
                                else:
                                    await db.money.update_one({'userid': user}, {'$inc': {f'fish.bait.{item["name"]}': amount}})
                                    await db.money.update_one({'userid': user}, {'$inc': {'balance': - (item['price'] * amount)}})
                                    await ctx.send(f"Congratulations on your new purchase of {amount} {item['name']}s! `{item['price'] * amount}Ᵽ` has been deducted from your account.")
                            else:
                                if person['balance'] < item['price']:
                                    await ctx.send('You need more money to buy that much.')
                                else:
                                    await db.money.update_one({'userid': user}, {'$inc': {f'fish.bait.{item["name"]}': 1}})
                                    await db.money.update_one({'userid': user}, {'$inc': {'balance': - item['price']}})
                                    await ctx.send(f"Congratulations on your new purchase of {item['name']}! `{item['price']}Ᵽ` has been deducted from your account.")
                elif item['name'] in inventory:
                    await ctx.send(f"You already own a {item['name']}")
                elif person['balance'] < item['price']:
                    await ctx.send("You do not have enough money to buy this.")
                else:
                    await db.money.update_one({'userid': user}, {'$push': {'inventory': item['name']}})
                    await db.money.update_one({'userid': user}, {'$inc': {'balance': - item['price']}})
                    await ctx.send(f"Congratulations on your new purchase of {item['name']}! `{item['price']}Ᵽ` has been deducted from your account.")
            # except Exception:
            #     await ctx.send("Something went wrong. Sorry. This is still WIP")
