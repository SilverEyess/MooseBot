import datetime
import random

from discord.ext import commands

from moosebot import MooseBot


class Pet:

    def __init__(self, bot: MooseBot):
        self.bot = bot

    @commands.command()
    async def train(self, ctx, pet=None):
        pets = ['dog', 'cat', 'custom pet']

        db = self.bot.database.db

        async def success(pet):
            db.pets.update({'$and': [{'userid': user}, {'pet_lower': pet.lower()}]},
                           {'$set': {'lasttrain': datetime.datetime.today()}})
            xp = random.randint(25, 75)
            await ctx.send(f"You train your {petlist[0]['pet']} and they gain {xp} xp.")
            db.pets.update({'$and': [{'userid': user}, {'pet_lower': pet.lower()}]}, {'$inc': {'xp': xp}}, True)
            if db.pets.find_one({'$and': [{'userid': user}, {'pet_lower': pet.lower()}]})['level'] is None:
                db.pets.update({'$and': [{'userid': user}, {'pet_lower': pet.lower()}]}, {'$set': {'level': 0}}, True)
            elif db.pets.find_one({'$and': [{'userid': user}, {'pet_lower': pet.lower()}]})['xp'] / 1000 != \
                    db.pets.find_one({'$and': [{'userid': user}, {'pet_lower': pet.lower()}]})['level']:
                petxp = db.pets.find_one({'$and': [{'userid': user}, {'pet_lower': pet.lower()}]})['xp']
                await ctx.send(f"Your {petlist[0]['pet']} has leveled up to {int(petxp / 1000)}. Congratulations!")
                db.pets.update({'$and': [{'userid': user}, {'pet_lower': pet.lower()}]},
                               {'$set': {'level': int(petxp / 1000)}}, True)

        user = str(ctx.author.id)
        pet = pet or None

        if pet is None:
            petlist = db.pets.find({'userid': str(ctx.author.id)})
            if petlist is None:
                await ctx.send("You have no pets to use this command on.")
            elif 'lasttrain' in db.pets.find_one({'$and': [{'userid': user}, {'pet': petlist[0]['pet']}]}):
                if db.pets.find_one({'$and': [{'userid': user}, {'pet': petlist[0]['pet']}]})[
                    'lasttrain'] + datetime.timedelta(days=1) < datetime.datetime.today():
                    await success(petlist[0]['petname_lower'])
                else:
                    timeleft = db.pets.find_one({'$and': [{'userid': user}, {'pet': petlist[0]['pet']}]})[
                                   'lasttrain'] + datetime.timedelta(hours=2) - datetime.datetime.today()
                    seconds = timeleft.total_seconds()
                    minutes = int((seconds % 3600) // 60)
                    hours = int(seconds // 3600)
                    await ctx.send(
                        f'You recently trained your pet. Please wait {f"{hours} hours and" if hours != 0 else ""} {minutes} to train again.')
            else:
                pet = petlist[0]['pet_lower']
                await success(pet)
        elif pet in pets:
            match = db.pets.find_one({'$and': [{'userid': user}, {'pet_lower': pet.lower()}]})
            if match is None:
                await ctx.send('You do not own that pet.')
            elif 'lasttrain' in db.pets.find_one({'$and': [{'userid': user}, {'pet_lower': pet.lower()}]}):
                if db.pets.find_one({'$and': [{'userid': user}, {'pet_lower': pet.lower()}]})[
                    'lasttrain'] + datetime.timedelta(days=1) < datetime.datetime.today():
                    await success(pet)
                else:
                    timeleft = db.pets.find_one({'$and': [{'userid': user}, {'pet_lower': pet.lower()}]})[
                                   'lasttrain'] + datetime.timedelta(hours=2) - datetime.datetime.today()
                    seconds = timeleft.total_seconds()
                    minutes = int((seconds % 3600) // 60)
                    hours = int(seconds // 3600)
                    await ctx.send(
                        f'You recently trained your pet. Please wait {f"{hours} hours and" if hours != 0 else ""} {minutes} to train again.')

        else:
            await ctx.send('There is no such pet.')
