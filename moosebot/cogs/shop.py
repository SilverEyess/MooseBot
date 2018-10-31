import asyncio

import discord
import pymongo
from discord.ext import commands

from moosebot import MooseBot


class Shop:

    def __init__(self, bot: MooseBot):
        self.bot = bot
        self.moneypath = "database/economy/money.json"

    @commands.command()
    @commands.check(MooseBot.is_owner)
    async def additem(self, ctx, price=None, *, item=None, ):
        item = item or None
        price = price or None
        shop = self.bot.database.db.shop
        if item is None:
            await ctx.send("Tell me what item you want to add, and at what price. `>additem item price`")
        elif price is None:
            await ctx.send("Tell me what item you want to add, and at what price. `>additem item price`")
        else:
            try:
                price = int(price)
                if price < 0:
                    await ctx.send("You can't set the price for an item to be 0 or less.")
                else:
                    await shop.insert_one({'name': item,
                                           'name_lower': item.lower(),
                                           'price': price})
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

    @commands.command()
    async def shop(self, ctx):
        shop = self.bot.database.db.shop
        pages = int((await shop.count_documents({})) / 9)
        embed = discord.Embed(title='MooseBot Shop.', colour=0xb18dff)
        amount1 = 0
        amount2 = 9
        order = 1
        async for i in shop.find(sort=[('price', pymongo.ASCENDING)])[amount1:amount2]:
            embed.add_field(name=f'#{order}: {i["name"]}', value=f'{i["price"]:,d}Ᵽ')
            order += 1
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
                        curpage += 1
                        embed.clear_fields()
                        amount1 += 9
                        amount2 += 9
                        async for i in await shop.find(sort=[('price', pymongo.ASCENDING)])[amount1:amount2]:
                            embed.add_field(name=f'#{order}: {i["name"]}', value=f'{i["price"]:,d}Ᵽ')
                            order += 1
                        await msg.edit(embed=embed)
                    await msg.remove_reaction(emoji='▶', member=ctx.author)
                elif str(reaction.emoji) == '◀' and user == ctx.author:
                    if curpage == 1:
                        await msg.remove_reaction(emoji='◀', member=ctx.author)
                        continue
                    else:
                        curpage -= 1
                        embed.clear_fields()
                        amount1 -= 9
                        amount2 -= 9
                        async for i in await shop.find(sort=[('price', pymongo.ASCENDING)])[amount1:amount2]:
                            embed.add_field(name=f'#{order}: {i["name"]}', value=f'{i["price"]:,d}Ᵽ')
                            order -= 1
                        await msg.edit(embed=embed)
                    await msg.remove_reaction(emoji='◀', member=ctx.author)

    @commands.command()
    @commands.check(MooseBot.is_owner)
    async def buy(self, ctx, *, item=None):
        db = self.bot.database.db
        shop = db.shop
        user = str(ctx.author.id)
        item = item or None
        pet_types = ['Dog', 'Cat', 'Custom Pet']
        if item is None:
            await ctx.send(
                "Please specify which item you want to buy, either by its name or number in the store. `>buy item`")
        else:
            try:
                item = int(item) - 1
                try:
                    item = await shop.find(sort=[('price', pymongo.ASCENDING)])[item]
                except Exception:
                    await ctx.send(f"There is no item #{item} on the store.")

            except ValueError:
                match = await shop.find_one({'name_lower': item.lower()})
                if match is None:
                    await ctx.send("That item does not exist on the store. For ease of use, use the item number.")
                else:
                    print(match)
                    item = match

            try:
                print(await db.money.find_one({'userid': user})['balance'])
                print(await db.money.find_one({'userid': user}))
                print(item['price'])
                if item['name'] in await db.money.find_one({'userid': user})['inventory']:
                    await ctx.send("You already own this item.")
                elif int(await db.money.find_one({'userid': user})['balance']) < int(item['price']):
                    await ctx.send("You do not have enough Ᵽlaceholders to purchase that item.")
                else:
                    if item['name'] in pet_types:
                        await db.pets.update_one({'userid': str(ctx.author.id)}, {'$set': {'pet': item['name']}}, True)
                        await db.pets.update_one({'userid': str(ctx.author.id)},
                                             {'$set': {'pet_lower': item['name'].lower()}}, True)
                        await db.pets.update_one({'userid': str(ctx.author.id)}, {'$set': {'level': 0}}, True)
                        await db.pets.update_one({'userid': str(ctx.author.id)}, {'$set': {'curhunger': 100}}, True)
                        await db.pets.update_one({'userid': str(ctx.author.id)}, {'$set': {'maxhunger': 100}}, True)
                        await db.money.update_one({'userid': user}, {'$push': {'inventory': item['name']}})
                        await db.money.update_one({'userid': user}, {'$inc': {'balance': -item['price']}})
                        await ctx.send(
                            f"Congratulations on your new purchase of {item['name']}! `{item['price']}Ᵽ` has been deducted from your account.")
                    else:
                        await db.money.update_one({'userid': user}, {'$push': {'inventory': item['name']}})
                        await db.money.update_one({'userid': user}, {'$inc': {'balance': -item['price']}})
                        await ctx.send(
                            f"Congratulations on your new purchase of {item['name']}! `{item['price']}Ᵽ` has been deducted from your account.")
            except KeyError:
                if item['name'] in pet_types:
                    await db.pets.update_one({'userid': str(ctx.author.id)}, {'$set': {'pet': item['name']}}, True)
                    await db.pets.update_one({'userid': str(ctx.author.id)}, {'$set': {'level': 0}}, True)
                    await db.pets.update_one({'userid': str(ctx.author.id)}, {'$set': {'curhunger': 100}}, True)
                    await db.pets.update_one({'userid': str(ctx.author.id)}, {'$set': {'maxhunger': 100}}, True)
                    await db.money.update_one({'userid': user}, {'$push': {'inventory': item['name']}})
                    await db.money.update_one({'userid': user}, {'$inc': {'balance': -item['price']}})
                    await ctx.send(
                        f"Congratulations on your new purchase of {item['name']}! `{item['price']}Ᵽ` has been deducted from your account.")
                else:
                    await db.money.update_one({'userid': user}, {'$push': {'inventory': item['name']}})
                    await db.money.update_one({'userid': user}, {'$inc': {'balance': -item['price']}})
                    await ctx.send(
                        f"Congratulations on your new purchase of {item['name']}! `{item['price']}Ᵽ` has been deducted from your account.")
