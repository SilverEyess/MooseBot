import asyncio
import random

import discord
from discord.ext import commands
from discord.ext.commands import Cog

from moosebot import MooseBot, converters, cog_group


@cog_group("Economy")
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

        try:

            person = await self.db.money.find_one({'userid': user})
            # if person is None:
            #     await MooseBot.generate(userid=user)
            if 'fish' in person:
                fishtable = person['fish']
                if 'curbait' in fishtable:
                    if fishtable['curbait'] == 'Game Bait':
                        if 'Game Bait' in fishtable['bait']:
                            if fishtable['bait']['Game Bait'] > 0:
                                if fishtable['bait']['Bait'] > 0:
                                    await self.db.money.update_one({'userid': user}, {'$inc': {f'fish.bait.{"Game Bait"}': -1}})

                                    if random.random() <= 0.01:

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

                                        # If there is no match (user has all trophies) then just award them 2000
                                        if match is None:
                                            await ctx.send(
                                                f"@here {ctx.author.mention} caught a trophy fish! However, it looks like you've already got a full collection. Take 20000{MooseBot.currency} anyway.")
                                            await self.db.money.update_one({'userid': user}, {'$inc': {'balance': 20000}}, True)
                                            await self.db.stats.update_one({'fishingstats': 'all'}, {'$inc': {'trophiescaught': 1}})
                                            return

                                        # Otherwise, tell them the fish they won, add it to their list of trophies and award them 2000
                                        else:
                                            await ctx.send(
                                                f"Well hot damn wait up a minute there bud. @here, {ctx.author.mention} just caught a trohpy fish! You caught a {match}! That's amazing tiger! Here's 20000{MooseBot.currency}")
                                            await self.db.money.update_one({'userid': user}, {'$inc': {'balance': 20000}}, True)
                                            await self.db.money.update_one({'userid': user}, {'$push': {'fish.trophies': match}})
                                            await self.db.stats.update_one({'fishingstats': 'all'}, {'$inc': {'trophiescaught': 1}})
                                            return

                    elif random.random() <= 0.003:

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

                        # If there is no match (user has all trophies) then just award them 2000
                        if match is None:
                            await ctx.send(f"@here {ctx.author.mention} caught a trophy fish! However, it looks like you've already got a full collection. Take 20000{MooseBot.currency} anyway.")
                            await self.db.money.update_one({'userid': user}, {'$inc': {'balance': 20000}}, True)
                            await self.db.stats.update_one({'fishingstats': 'all'}, {'$inc': {'trophiescaught': 1}})
                            return

                        # Otherwise, tell them the fish they won, add it to their list of trophies and award them 2000
                        else:
                            await ctx.send(f"Well hot damn wait up a minute there bud. @here, {ctx.author.mention} just caught a trohpy fish! You caught a {match}! That's amazing tiger! Here's 20000{MooseBot.currency}")
                            await self.db.money.update_one({'userid': user}, {'$inc': {'balance': 20000}}, True)
                            await self.db.money.update_one({'userid': user}, {'$push': {'fish.trophies': match}})
                            await self.db.stats.update_one({'fishingstats': 'all'}, {'$inc': {'trophiescaught': 1}})
                            return
                elif random.random() <= 0.003:

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

                    # If there is no match (user has all trophies) then just award them 2000
                    if match is None:
                        await ctx.send(
                            f"@here {ctx.author.mention} caught a trophy fish! However, it looks like you've already got a full collection. Take 20000{MooseBot.currency} anyway.")
                        await self.db.money.update_one({'userid': user}, {'$inc': {'balance': 20000}}, True)
                        await self.db.stats.update_one({'fishingstats': 'all'}, {'$inc': {'trophiescaught': 1}})
                        return

                    # Otherwise, tell them the fish they won, add it to their list of trophies and award them 2000
                    else:
                        await ctx.send(
                            f"Well hot damn wait up a minute there bud. @here, {ctx.author.mention} just caught a trohpy fish! You caught a {match}! That's amazing tiger! Here's 20000{MooseBot.currency}")
                        await self.db.money.update_one({'userid': user}, {'$inc': {'balance': 20000}}, True)
                        await self.db.money.update_one({'userid': user}, {'$push': {'fish.trophies': match}})
                        await self.db.stats.update_one({'fishingstats': 'all'}, {'$inc': {'trophiescaught': 1}})
                        return

            '''
            Catch the exception if the user does not have the 'trophylist' entry in their database entry and give them 
            a random trophy and 2000 
            '''
        except KeyError:
            trophy = random.choice(trophy_fish)
            await ctx.send(f"Well hot damn wait up a minute there bud. @here, {ctx.author.mention} just caught a trohpy fish! You caught a {trophy}! That's amazing tiger! Here's 20000{MooseBot.currency}")
            await self.db.money.update_one({'userid': user}, {'$push': {'fish.trophies': trophy}})
            await self.db.money.update_one({'userid': user}, {'$inc': {'balance': 20000}}, True)
            await self.db.stats.update_one({'fishingstats': 'all'}, {'$inc': {'trophiescaught': 1}})
            return

        '''
        If the user didn't get a trophy fish, the following code gets ran. Roll a number to determine the size range of
        the fish they catch and store it. Compare the number and when it matches the criteria, roll for a random weight
        in the range provided and store it.
        '''

        table = await self.db.money.find_one({'userid': str(user)})
        if table is None:
            await ctx.send('You need bait to fish pal.')
            self.cast.reset_cooldown(ctx)
            return
        elif 'fish' not in table:
            await ctx.send('You need bait to fish pal.')
            self.cast.reset_cooldown(ctx)
            return
        fishtable = table['fish']

        async def regular_roll(roll):
            if roll == 69:
                weight = random.randint(70000, 80000)
            elif roll <= 5:
                weight = random.randint(1, 5000)
            elif roll <= 15:
                weight = random.randint(5001, 10000)
            elif roll <= 30:
                weight = random.randint(10001, 25000)
            elif roll <= 45:
                weight = random.randint(25001, 45000)
            elif roll <= 60:
                weight = random.randint(45001, 60000)
            elif roll <= 70:
                weight = random.randint(60001, 75000)
            elif roll <= 85:
                weight = random.randint(75001, 85000)
            elif roll <= 99:
                weight = random.randint(85001, 90000)
            elif roll == 100:
                weight = random.randint(90000, 101623)
            return weight

        roll = random.randint(1, 100)

        if 'rod' in fishtable:
            if fishtable['rod'] is 'None':
                roll = random.randint(1, 100)
            else:
                if fishtable['rod'] == 'Copper Rod':
                    roll = random.randint(3, 100)
                elif fishtable['rod'] == 'Bronze Rod':
                    roll = random.randint(6, 100)
                elif fishtable['rod'] == 'Silver Rod':
                    roll = random.randint(10, 100)
                elif fishtable['rod'] == 'Gold Rod':
                    roll = random.randint(20, 100)
                elif fishtable['rod'] == 'Diamond Rod':
                    roll = random.randint(31, 100)
                elif fishtable['rod'] == 'Jewelled Rod':
                    roll = random.randint(40, 100)
                elif fishtable['rod'] == 'Elite Rod':
                    roll = random.randint(50, 100)
        else:
            roll = random.randint(1, 100)

        if 'bait' in fishtable:
            if 'Bait' in fishtable['bait']:
                if fishtable['bait']['Bait'] > 0:
                    await self.db.money.update_one({'userid': user}, {'$inc': {f'fish.bait.{"Bait"}': -1}})
                    weight = await regular_roll(roll)
                else:
                    await ctx.send("You need to buy some bait to fish my guy.")
                    self.cast.reset_cooldown(ctx)
                    return
            else:
                await ctx.send("You need to buy bait to fish.")
                self.cast.reset_cooldown(ctx)
                return
        else:
            await ctx.send("You need to buy bait to fish.")
            self.cast.reset_cooldown(ctx)
            return

        try:
            fishtable = await self.db.money.find_one({'userid': user}, {'fish.largestfish'})

            if 'fish' not in await self.db.money.find_one({'userid': user}):
                await ctx.send(f"{ctx.author.display_name} used a bait and caught a fish weighing {f'{weight / 1000}kg.' if weight > 1000 else f'{weight}g.'} {random.choice(fish)}")
                await self.db.money.update_one({'userid': user}, {'$inc': {'fish.totalweight': weight}})
                await self.db.money.update_one({'userid': user}, {'$set': {'fish.largestfish': weight}})
                await self.db.money.update_one({'userid': user}, {'$set': {'fish.recentfish': weight}})
                await self.db.money.update_one({'userid': user}, {'$inc': {'fish.totalfish': 1}})
                await self.db.money.update_one({'userid': user}, {'$inc': {'fish.sincelastsell': 1}})
                await ctx.send("Wow, that's one big fish! Infact, it's the largest one you've caught! Congratulations!")
                await self.db.stats.update_one({'fishingstats': 'all'}, {'$inc': {'moneyspentoncast': 80}})
                await self.db.stats.update_one({'fishingstats': 'all'}, {'$inc': {'totalweightcaught': weight}})
                await self.db.stats.update_one({'fishingstats': 'all'}, {'$inc': {'totalworthcaught': int(weight * 0.0025)}})
                await self.db.stats.update_one({'fishingstats': 'all'}, {'$inc': {'totalfishcaught': 1}})
                return

            elif weight > fishtable['fish']['largestfish']:
                await ctx.send(f"{ctx.author.display_name} used a bait and caught a fish weighing {f'{weight / 1000}kg.' if weight > 1000 else f'{weight}g.'} {random.choice(fish)}")
                await ctx.send("Wow, that's one big fish! Infact, it's the largest one you've caught! Congratulations!")
                await self.db.money.update_one({'userid': user}, {'$inc': {'fish.totalweight': weight}})
                await self.db.money.update_one({'userid': user}, {'$set': {'fish.largestfish': weight}})
                await self.db.money.update_one({'userid': user}, {'$set': {'fish.recentfish': weight}})
                await self.db.money.update_one({'userid': user}, {'$inc': {'fish.totalfish': 1}})
                await self.db.money.update_one({'userid': user}, {'$inc': {'fish.sincelastsell': 1}})
                await self.db.stats.update_one({'fishingstats': 'all'}, {'$inc': {'moneyspentoncast': 80}})
                await self.db.stats.update_one({'fishingstats': 'all'}, {'$inc': {'totalweightcaught': weight}})
                await self.db.stats.update_one({'fishingstats': 'all'}, {'$inc': {'totalworthcaught': int(weight * 0.0025)}})
                await self.db.stats.update_one({'fishingstats': 'all'}, {'$inc': {'totalfishcaught': 1}})

            else:
                await ctx.send(f"{ctx.author.display_name} used a bait and caught a fish weighing {f'{weight/1000}kg.' if weight > 1000 else f'{weight}g.'} {random.choice(fish)}")
                await self.db.money.update_one({'userid': user}, {'$inc': {'fish.totalweight': weight}})
                await self.db.money.update_one({'userid': user}, {'$set': {'fish.recentfish': weight}})
                await self.db.money.update_one({'userid': user}, {'$inc': {'fish.totalfish': 1}})
                await self.db.money.update_one({'userid': user}, {'$inc': {'fish.sincelastsell': 1}})
                await self.db.stats.update_one({'fishingstats': 'all'}, {'$inc': {'moneyspentoncast': 80}})
                await self.db.stats.update_one({'fishingstats': 'all'}, {'$inc': {'totalweightcaught': weight}})
                await self.db.stats.update_one({'fishingstats': 'all'}, {'$inc': {'totalworthcaught': int(weight * 0.0025)}})
                await self.db.stats.update_one({'fishingstats': 'all'}, {'$inc': {'totalfishcaught': 1}})

        except Exception:
            await ctx.send(f"{ctx.author.display_name} spent 80{MooseBot.currency} and caught a fish weighing {f'{weight/1000}kg.' if weight > 1000 else f'{weight}g.'} {random.choice(fish)}")
            await self.db.money.update_one({'userid': user}, {'$inc': {'fish.totalweight': weight}})
            await self.db.money.update_one({'userid': user}, {'$set': {'fish.largestfish': weight}})
            await self.db.money.update_one({'userid': user}, {'$set': {'fish.recentfish': weight}})
            await self.db.money.update_one({'userid': user}, {'$inc': {'fish.totalfish': 1}})
            await self.db.money.update_one({'userid': user}, {'$inc': {'fish.sincelastsell': 1}})
            await self.db.money.update_one({'userid': user}, {'$inc': {'balance': -80}}, True)
            await self.db.stats.update_one({'fishingstats': 'all'}, {'$inc': {'moneyspentoncast': 80}})
            await self.db.stats.update_one({'fishingstats': 'all'}, {'$inc': {'totalweightcaught': weight}})
            await self.db.stats.update_one({'fishingstats': 'all'}, {'$inc': {'totalworthcaught': int(weight * 0.0025)}})
            await self.db.stats.update_one({'fishingstats': 'all'}, {'$inc': {'totalfishcaught': 1}})
            await ctx.send("Wow, that's one big fish! Infact, it's the largest one you've caught! Congratulations!")

    @cast.error
    async def cast_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            seconds = int(error.retry_after % 60)
            minutes = int((error.retry_after % 3600) // 60)
            await ctx.send(f"You cannot fish for another {f'{minutes} minutes and {seconds} seconds.' if minutes != 0 else f'{seconds} seconds'}")
        else:
            print(error)

    @commands.command(aliases=['setbait', 'sb'])
    async def selectbait(self, ctx, *, bait=None):
        bait = bait.title() or None
        baittypes = ['Bait', 'Large Bait', 'Game Bait']
        if bait is None:
            await ctx.send("You need to pick a type of bait to use.")
        elif bait not in baittypes:
            await ctx.send("That's not a type of bait.")
        else:
            await self.db.money.update_one({'userid': str(ctx.author.id)}, {'$set': {'fish.curbait': bait}})
            await ctx.send(f'Your current bait is now {bait}.')

    @commands.command()
    async def fish(self, ctx, user: converters.PartialMember = None):
        user = user or None
        if user is None:
            user = ctx.author
        else:
            user = user
        try:
            table = await self.db.money.find_one({'userid': str(user.id)})
            if table is None:
                await ctx.send("This person doesn't exist to me")
                return
            if 'fish' not in table:
                await ctx.send("This user has not participated in any fishing yet.")
                return
            else:
                fishtable = table['fish']
                fishweight = fishtable['totalweight']
                fishlargest = fishtable['largestfish']
                fishrecent = fishtable['recentfish']
                fishtotal = fishtable['totalfish']
                fishsincesell = fishtable['sincelastsell']
                fishvalue = int(fishtable['totalweight'] * 0.0025)
                if 'trophies' not in fishtable:
                    description = f"✴**Largest fish:** {f'{fishlargest / 1000}kg.' if fishlargest > 1000 else f'{fishlargest}g.'}\n" \
                        f"✴**Total fish weight:** {f'{fishweight / 1000}kg.' if fishweight > 1000 else f'{fishweight}g.'}\n" \
                        f"✴**Most recent fish:** {f'{fishrecent / 1000}kg.' if fishrecent > 1000 else f'{fishrecent}g.'}\n" \
                        f"✴**Total fish caught:** {fishtotal}\n" \
                        f"✴**Fish caught since last sell:** {fishsincesell}\n" \
                        f"✴**Current fish sell price:** {fishvalue}{MooseBot.currency}"

                else:
                    trophytable = fishtable['trophies']
                    trophies = ', '.join(map(str, trophytable))
                    description = f"✴**Largest fish:** {f'{fishlargest/1000}kg.' if fishlargest > 1000 else f'{fishlargest}g.'}\n" \
                        f"✴**Total fish weight:** {f'{fishweight/1000}kg.' if fishweight > 1000 else f'{fishweight}g.'}\n" \
                        f"✴**Most recent fish:** {f'{fishrecent/1000}kg.' if fishrecent > 1000 else f'{fishrecent}g.'}\n" \
                        f"✴**Total fish caught:** {fishtotal}\n" \
                        f"✴**Fish caught since last sell:** {fishsincesell}\n" \
                        f"✴**Current fish sell price:** {fishvalue}{MooseBot.currency}\n" \
                        f"✴**Trophies:**\n {trophies}"

                value = ""
                if 'rod' in fishtable:
                    value += f"✴**Current Rod:** {'Standard' if fishtable['rod'] == 'None' else fishtable['rod']}\n"
                if 'curbait' in fishtable:
                    value += f"✴**Current Bait:** {'Standard' if fishtable['curbait'] == 'None' else fishtable['curbait']}\n"
                baittotal = 0
                if 'bait' in fishtable:
                    baitstats = ""

                    for i in fishtable['bait']:
                        baitstats += f"✴**{i}:** {fishtable['bait'][i]}\n"
                        baittotal += fishtable['bait'][i]
                    value += f"{baitstats}"

                if 'inventory' in table:
                    if 'Bait Bucket' in table['inventory']:
                        value += f'✴**Maximum bait capacity:** {f"{baittotal}" if not 0 else 0}/300'
                    else:
                        value += f'✴**Maximum bait capacity:** {f"{baittotal}" if not 0 else 0}/100'
                embed = discord.Embed(title=f"{user.display_name}'s fishing stats.", description=description, colour=0xb18dff)
                embed.add_field(name='**Item Stats**', value=value)
                embed.set_thumbnail(url=user.avatar_url_as(format='png'))
                await ctx.send(embed=embed)

        except AttributeError:
            await ctx.send("Sorry buckaroo. Haven't seen that person around here. Perhaps they don't exist?")

        except Exception:
            if user is not ctx.author:
                await ctx.send("Well gosh darn. Looks like that person has not cast a line yet. Tell them to get to it!")
            else:
                await ctx.send("Well gosh darn bud. Looks like you've not cast a line yet. Get to it!")

    # @commands.check(MooseBot.is_owner)
    @commands.command(aliases=['select', 'sr'])
    async def selectrod(self, ctx, *, rod):
        user = str(ctx.author.id)
        rod = rod.title() or None
        rod_types = ['Copper Rod', 'Bronze Rod', 'Silver Rod', 'Gold Rod', 'Diamond Rod', 'Jewelled Rod', 'Elite Rod']
        if rod is None:
            await ctx.send("You need to select a rod to use.")
        elif rod not in rod_types:
            await ctx.send("That's not a valid rod pal.")
        try:
            person = await self.db.money.find_one({'userid': user})
            inventory = person['inventory']
            if rod not in inventory:
                await ctx.send("Aww man, maybe one day you'll be able to afford that rod. But looks like you don't have it right now kiddo.")
            elif 'rod' not in person['fish']:
                await self.db.money.update_one({'userid': user}, {'$set': {'fish.rod': rod}})
                await ctx.send(f"You're now using your {rod}.")

            elif person['fish']['rod'] == rod:
                await ctx.send("You were already using that rod mate.")
            else:
                await self.db.money.update_one({'userid': user}, {'$set': {'fish.rod': rod}})
                await ctx.send(f"You're now using your {rod}.")

        except Exception:
            await ctx.send("Looks like you don't own that rod bud. Sorry.")

    @commands.command(aliases=['sf', 'shellfish'])
    async def sellfish(self, ctx):
        user = str(ctx.author.id)
        try:
            table = await self.db.money.find_one({'userid': user}, {'fish'})
            fishtable = table['fish']
            fishweight = fishtable['totalweight']
            fishamount = fishtable['sincelastsell']
            average = float(fishweight / fishamount)
            if fishweight == 0:
                await ctx.send("Well golly. Looks like you're all out of fish. Time to get on the water again!")
            else:
                money = int(fishweight * 0.0025)
                await ctx.send(f"You just sold {f'{fishamount} fish, weighing a total {fishweight/1000}kg (avg.{int(average/1000)}kg) ' if fishweight > 1000 else f'{fishamount} fish, weighing a total {fishweight}g (avg.{average}g) '} for {money}Ᵽ. Come back again!")
                await self.db.money.update_one({'userid': user}, {'$set': {'fish.totalweight': 0}})
                await self.db.money.update_one({'userid': user}, {'$inc': {'balance': money}}, True)
                await self.db.money.update_one({'userid': user}, {'$set': {'fish.sincelastsell': 0}})
                await self.db.stats.update_one({'fishingstats': 'all'}, {'$inc': {'moneyfromfishsells': money}})

        except Exception:
            await ctx.send("Well golly. Looks like you're all out of fish. Time to get on the water again!")


def setup(bot):
    bot.add_cog(Fishing(bot.moose))
