import asyncio
import random

import discord
from discord.ext import commands
from discord.ext.commands import Cog

from moosebot import MooseBot, converters


class Fishing(Cog):

    def __init__(self, bot: MooseBot):
        self.bot = bot
        self.db = self.bot.database.db

    @commands.command()
    @commands.cooldown(1, 300, commands.BucketType.user)
    async def cast(self, ctx):
        fish = ["🐟", "🐠", "🐡", "🎣"]
        user = str(ctx.author.id)
        roll = random.randint(1, 100)
        if roll == 69:
            weight = random.randint(16001, 20000)
        elif roll <= 10:
            weight = random.randint(30, 700)
        elif roll <= 25:
            weight = random.randint(701, 2000)
        elif roll <= 45:
            weight = random.randint(2001, 4000)
        elif roll <= 65:
            weight = random.randint(4001, 9000)
        elif roll <= 80:
            weight = random.randint(9001, 16000)
        elif roll <= 90:
            weight = random.randint(16001, 23000)
        elif roll <= 99:
            weight = random.randint(23001, 30000)
        elif roll <= 100:
            weight = random.randint(30001, 33000)
        await ctx.send(f"You spent 150Ᵽ and caught a fish weighing {f'{weight/1000}kg.' if weight > 1000 else f'{weight}g.'} {random.choice(fish)}")
        try:
            fishtable = await self.db.money.find_one({'userid': user}, {'fish.largestfish'})
            bal = await self.db.money.find_one({'userid': user})
            if 150 > bal['balance']:
                await ctx.send('You need at least 150Ᵽ to fish pal.')
                return
            elif 'fish' not in await self.db.money.find_one({'userid': user}):
                await self.db.money.update_one({'userid': user}, {'$inc': {'fish.totalweight': weight}})
                await self.db.money.update_one({'userid': user}, {'$set': {'fish.largestfish': weight}})
                await self.db.money.update_one({'userid': user}, {'$set': {'fish.recentfish': weight}})
                await self.db.money.update_one({'userid': user}, {'$inc': {'balance': -150}}, True)
                await ctx.send("Wow, that's one big fish! Infact, it's the largest one you've caught! Congratulations!")
                return

            if weight > fishtable['fish']['largestfish']:
                await ctx.send("Wow, that's one big fish! Infact, it's the largest one you've caught! Congratulations!")
                await self.db.money.update_one({'userid': user}, {'$inc': {'fish.totalweight': weight}})
                await self.db.money.update_one({'userid': user}, {'$set': {'fish.largestfish': weight}})
                await self.db.money.update_one({'userid': user}, {'$set': {'fish.recentfish': weight}})
                await self.db.money.update_one({'userid': user}, {'$inc': {'balance': -150}}, True)

            else:
                await self.db.money.update_one({'userid': user}, {'$inc': {'fish.totalweight': weight}})
                await self.db.money.update_one({'userid': user}, {'$set': {'fish.recentfish': weight}})
                await self.db.money.update_one({'userid': user}, {'$inc': {'balance': -150}}, True)

        except Exception:
            await self.db.money.update_one({'userid': user}, {'$inc': {'fish.totalweight': weight}})
            await self.db.money.update_one({'userid': user}, {'$set': {'fish.largestfish': weight}})
            await self.db.money.update_one({'userid': user}, {'$set': {'fish.recentfish': weight}})
            await self.db.money.update_one({'userid': user}, {'$inc': {'balance': -150}}, True)
            await ctx.send("Wow, that's one big fish! Infact, it's the largest one you've caught! Congratulations!")
            return

    @cast.error
    async def cast_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            seconds = int(error.retry_after % 60)
            minutes = int((error.retry_after % 3600) // 60)
            await ctx.send(f"You cannot fish for another {f'{minutes} minutes and {seconds} seconds.' if minutes != 0 else f'{seconds} seconds'}")

    @commands.command()
    async def fish(self, ctx):
        user = str(ctx.author.id)
        try:
            table = await self.db.money.find_one({'userid': user}, {'fish'})
            fishtable = table['fish']
            fishweight = fishtable['totalweight']
            fishlargest = fishtable['largestfish']
            fishrecent = fishtable['recentfish']
            description = f"✴**Largest fish:** {f'{fishlargest/1000}kg.' if fishlargest > 1000 else f'{fishlargest}g.'}\n" \
                f"✴**Total fish weight:** {f'{fishweight/1000}kg.' if fishweight > 1000 else f'{fishweight}g.'}\n " \
                f"✴**Most recent fish:** {f'{fishrecent/1000}kg.' if fishrecent > 1000 else f'{fishrecent}g.'}\n"
            embed = discord.Embed(title=f"{ctx.author.display_name}'s fishing stats.", description=description, colour=0xb18dff)
            await ctx.send(embed=embed)

        except Exception:
            await ctx.send("Well gosh darn bud. Looks like you've not cast a line yet. Get to it!")

    @commands.command()
    async def sellfish(self, ctx):
        user = str(ctx.author.id)
        try:
            table = await self.db.money.find_one({'userid': user}, {'fish'})
            fishtable = table['fish']
            fishweight = fishtable['totalweight']
            money = int(fishweight * 0.02)
            await ctx.send(f"You just sold {f'{fishweight/1000}kg ' if fishweight > 1000 else f'{fishweight}g '}of fish for {money}Ᵽ. Come back again!")
            await self.db.money.update_one({'userid': user}, {'$set': {'fish.totalweight': 0}})
            await self.db.money.update_one({'userid': user}, {'$inc': {'balance': money}}, True)

        except Exception:
            await ctx.send("Well golly. Looks like you're all out of fish. Time to get on the water again!")


