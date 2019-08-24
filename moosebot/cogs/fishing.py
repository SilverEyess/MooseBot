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
    # @commands.check(MooseBot.is_owner)
    @commands.cooldown(1, 300, commands.BucketType.user)
    async def cast(self, ctx):
        # Define table for fish emojis and trophy fish, more trophy fish can be added but just adding to the table.
        fish = ["🐟", "🐠", "🐡"]
        trophy_fish = ["🎣", "🦍", "👃🏿", "🌰", "👺", "👹", "💩", "🎅", "👅", "🗣", "👌", "👊", "🤙", "🐋", "🐳", "🍄", "🦑", "🦅", "🍆", "🍌", "🍑", "🍒", "🥝", "🕋", "🗿", "♋"]

        # Define user's id as a string for later use.
        user = str(ctx.author.id)

        # Roll for chance to get a trophy fish and define winning rolls for trophy fish.
        trophyroll = random.randint(1, 10000)
        wins = ['69', '696', '6969', '7483', '1', '2', '1453', '16', '1624', '5428']

        try:

            # Checks if rolled a winning number for a trophy fish.
            if trophyroll in wins:

                # Get and define the users entry in database that stores their fish and other profile information.
                dblist = await self.db.money.find_one({'userid': user}, {'fish.trophies'})
                # Get list of users trophies (if any) and define it
                trophies = dblist['fish']['trophies']
                # Shuffle the list of possible trophy fish to randomise order.
                random.shuffle(trophy_fish)
                '''
                 Compare list of users trophies(if any) against the list of possible trophy fish and get the first 
                 trophy that the user doesn't have already and store that as 'match'.
                '''
                match = next(iter([i for i in trophy_fish if i not in trophies]), None)
                # If there is no match (user has all trophies) then just award them 2000Ᵽ
                if match is None:
                    await ctx.send("You caught a trophy fish but it looks like you've already got a full collection. Take 2000Ᵽ anyway.")
                    await self.db.money.update_one({'userid': user}, {'$inc': {'balance': 2000}}, True)
                    await self.db.stats.update_one({'fishingstats': 'all'}, {'$inc': {'trophiescaught': 1}})
                    return

                # Otherwise, tell them the fish they won, add it to their list of trophies and award them 2000Ᵽ
                else:
                    await ctx.send(f"Well hot damn wait up a minute there bud. You just caught a trohpy fish! You caught a {match}! That's amazing tiger! Here's 2000Ᵽ")
                    await self.db.money.update_one({'userid': user}, {'$inc': {'balance': 2000}}, True)
                    await self.db.money.update_one({'userid': user}, {'$push': {'fish.trophies': match}})
                    await self.db.stats.update_one({'fishingstats': 'all'}, {'$inc': {'trophiescaught': 1}})
                    return

            '''
            Catch the exception if the user does not have the 'trophylist' entry in their database entry and give them 
            a random trophy and 2000Ᵽ 
            '''
        except KeyError:
            trophy = random.choice(trophy_fish)
            await ctx.send(f"Well hot damn wait up a minute there bud. You just caught a trohpy fish! You caught a {trophy}! That's amazing tiger! Here's 2000Ᵽ")
            await self.db.money.update_one({'userid': user}, {'$push': {'fish.trophies': trophy}})
            await self.db.money.update_one({'userid': user}, {'$inc': {'balance': 2000}}, True)
            await self.db.stats.update_one({'fishingstats': 'all'}, {'$inc': {'trophiescaught': 1}})
            return

        '''
        If the user didn't get a trophy fish, the following code gets ran. Roll a number to determine the size range of
        the fish they catch and store it. Compare the number and when it matches the criteria, roll for a random weight
        in the range provided and store it.
        '''

        roll = random.randint(1, 100)
        if roll == 69:
            weight = random.randint(16001, 20000)
        elif roll <= 10:
            weight = random.randint(30, 700)
        elif roll <= 25:
            weight = random.randint(701, 2000)
        elif roll <= 45:
            weight = random.randint(2001, 8000)
        elif roll <= 65:
            weight = random.randint(8001, 14000)
        elif roll <= 80:
            weight = random.randint(14001, 20000)
        elif roll <= 90:
            weight = random.randint(20001, 23000)
        elif roll <= 99:
            weight = random.randint(23001, 30000)
        elif roll <= 100:
            weight = random.randint(30001, 33000)

        try:
            fishtable = await self.db.money.find_one({'userid': user}, {'fish.largestfish'})
            bal = await self.db.money.find_one({'userid': user})
            if 80 > bal['balance']:
                await ctx.send('You need at least 80Ᵽ to fish pal.')

            elif 'fish' not in await self.db.money.find_one({'userid': user}):
                await ctx.send(f"You spent 80Ᵽ and caught a fish weighing {f'{weight / 1000}kg.' if weight > 1000 else f'{weight}g.'} {random.choice(fish)}")
                await self.db.money.update_one({'userid': user}, {'$inc': {'fish.totalweight': weight}})
                await self.db.money.update_one({'userid': user}, {'$set': {'fish.largestfish': weight}})
                await self.db.money.update_one({'userid': user}, {'$set': {'fish.recentfish': weight}})
                await self.db.money.update_one({'userid': user}, {'$inc': {'fish.totalfish': 1}})
                await self.db.money.update_one({'userid': user}, {'$inc': {'fish.sincelastsell': 1}})
                await self.db.money.update_one({'userid': user}, {'$inc': {'balance': -80}}, True)
                await ctx.send("Wow, that's one big fish! Infact, it's the largest one you've caught! Congratulations!")
                await self.db.stats.update_one({'fishingstats': 'all'}, {'$inc': {'moneyspentoncast': 80}})
                await self.db.stats.update_one({'fishingstats': 'all'}, {'$inc': {'totalweightcaught': weight}})
                await self.db.stats.update_one({'fishingstats': 'all'}, {'$inc': {'totalworthcaught': int(weight * 0.02)}})
                await self.db.stats.update_one({'fishingstats': 'all'}, {'$inc': {'totalfishcaught': 1}})

            if weight > fishtable['fish']['largestfish']:
                await ctx.send(f"You spent 80Ᵽ and caught a fish weighing {f'{weight / 1000}kg.' if weight > 1000 else f'{weight}g.'} {random.choice(fish)}")
                await ctx.send("Wow, that's one big fish! Infact, it's the largest one you've caught! Congratulations!")
                await self.db.money.update_one({'userid': user}, {'$inc': {'fish.totalweight': weight}})
                await self.db.money.update_one({'userid': user}, {'$set': {'fish.largestfish': weight}})
                await self.db.money.update_one({'userid': user}, {'$set': {'fish.recentfish': weight}})
                await self.db.money.update_one({'userid': user}, {'$inc': {'fish.totalfish': 1}})
                await self.db.money.update_one({'userid': user}, {'$inc': {'fish.sincelastsell': 1}})
                await self.db.money.update_one({'userid': user}, {'$inc': {'balance': -80}}, True)
                await self.db.stats.update_one({'fishingstats': 'all'}, {'$inc': {'moneyspentoncast': 80}})
                await self.db.stats.update_one({'fishingstats': 'all'}, {'$inc': {'totalweightcaught': weight}})
                await self.db.stats.update_one({'fishingstats': 'all'}, {'$inc': {'totalworthcaught': int(weight * 0.02)}})
                await self.db.stats.update_one({'fishingstats': 'all'}, {'$inc': {'totalfishcaught': 1}})

            else:
                await ctx.send(f"You spent 80Ᵽ and caught a fish weighing {f'{weight/1000}kg.' if weight > 1000 else f'{weight}g.'} {random.choice(fish)}")
                await self.db.money.update_one({'userid': user}, {'$inc': {'fish.totalweight': weight}})
                await self.db.money.update_one({'userid': user}, {'$set': {'fish.recentfish': weight}})
                await self.db.money.update_one({'userid': user}, {'$inc': {'fish.totalfish': 1}})
                await self.db.money.update_one({'userid': user}, {'$inc': {'fish.sincelastsell': 1}})
                await self.db.money.update_one({'userid': user}, {'$inc': {'balance': -80}}, True)
                await self.db.stats.update_one({'fishingstats': 'all'}, {'$inc': {'moneyspentoncast': 80}})
                await self.db.stats.update_one({'fishingstats': 'all'}, {'$inc': {'totalweightcaught': weight}})
                await self.db.stats.update_one({'fishingstats': 'all'}, {'$inc': {'totalworthcaught': int(weight * 0.02)}})
                await self.db.stats.update_one({'fishingstats': 'all'}, {'$inc': {'totalfishcaught': 1}})

        except Exception:
            await ctx.send(f"You spent 80Ᵽ and caught a fish weighing {f'{weight/1000}kg.' if weight > 1000 else f'{weight}g.'} {random.choice(fish)}")
            await self.db.money.update_one({'userid': user}, {'$inc': {'fish.totalweight': weight}})
            await self.db.money.update_one({'userid': user}, {'$set': {'fish.largestfish': weight}})
            await self.db.money.update_one({'userid': user}, {'$set': {'fish.recentfish': weight}})
            await self.db.money.update_one({'userid': user}, {'$inc': {'fish.totalfish': 1}})
            await self.db.money.update_one({'userid': user}, {'$inc': {'fish.sincelastsell': 1}})
            await self.db.money.update_one({'userid': user}, {'$inc': {'balance': -80}}, True)
            await self.db.stats.update_one({'fishingstats': 'all'}, {'$inc': {'moneyspentoncast': 80}})
            await self.db.stats.update_one({'fishingstats': 'all'}, {'$inc': {'totalweightcaught': weight}})
            await self.db.stats.update_one({'fishingstats': 'all'}, {'$inc': {'totalworthcaught': int(weight * 0.02)}})
            await self.db.stats.update_one({'fishingstats': 'all'}, {'$inc': {'totalfishcaught': 1}})
            await ctx.send("Wow, that's one big fish! Infact, it's the largest one you've caught! Congratulations!")

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
            fishtotal = fishtable['totalfish']
            fishsincesell = fishtable['sincelastsell']
            if 'trophies' not in fishtable:
                description = f"✴**Largest fish:** {f'{fishlargest / 1000}kg.' if fishlargest > 1000 else f'{fishlargest}g.'}\n" \
                    f"✴**Total fish weight:** {f'{fishweight / 1000}kg.' if fishweight > 1000 else f'{fishweight}g.'}\n" \
                    f"✴**Most recent fish:** {f'{fishrecent / 1000}kg.' if fishrecent > 1000 else f'{fishrecent}g.'}\n" \
                    f"✴**Total fish caught:** {fishtotal}\n" \
                    f"✴**Fish caught since last sell:** {fishsincesell}\n"

            else:
                trophytable = fishtable['trophies']
                trophies = ', '.join(map(str, trophytable))
                description = f"✴**Largest fish:** {f'{fishlargest/1000}kg.' if fishlargest > 1000 else f'{fishlargest}g.'}\n" \
                    f"✴**Total fish weight:** {f'{fishweight/1000}kg.' if fishweight > 1000 else f'{fishweight}g.'}\n" \
                    f"✴**Most recent fish:** {f'{fishrecent/1000}kg.' if fishrecent > 1000 else f'{fishrecent}g.'}\n" \
                    f"✴**Total fish caught:** {fishtotal}\n" \
                    f"✴**Fish caught since last sell:** {fishsincesell}\n" \
                    f"✴**Trophies:**\n {trophies}"

            embed = discord.Embed(title=f"{ctx.author.display_name}'s fishing stats.", description=description, colour=0xb18dff)
            await ctx.send(embed=embed)

        except Exception:
            await ctx.send("Well gosh darn bud. Looks like you've not cast a line yet. Get to it!")

    @commands.command()
    async def sellfish(self, ctx):
        user = str(ctx.author.id)
        # try:
        table = await self.db.money.find_one({'userid': user}, {'fish'})
        fishtable = table['fish']
        fishweight = fishtable['totalweight']
        money = int(fishweight * 0.02)
        if fishweight == 0:
            await ctx.send("Well golly. Looks like you're all out of fish. Time to get on the water again!")
        else:
            await ctx.send(f"You just sold {f'{fishweight/1000}kg ' if fishweight > 1000 else f'{fishweight}g '}of fish for {money}Ᵽ. Come back again!")
            await self.db.money.update_one({'userid': user}, {'$set': {'fish.totalweight': 0}})
            await self.db.money.update_one({'userid': user}, {'$inc': {'balance': money}}, True)
            await self.db.money.update_one({'userid': user}, {'$set': {'fish.sincelastsell': 0}})
            await self.db.stats.update_one({'fishingstats': 'all'}, {'$inc': {'moneyfromfishsells': money}})

        # except Exception:
        #     await ctx.send("Well golly. Looks like you're all out of fish. Time to get on the water again!")


