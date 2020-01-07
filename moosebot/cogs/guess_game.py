import random

from discord.ext import commands
from discord.ext.commands import Cog

from moosebot import MooseBot, cog_group


@cog_group("Interactive")
class GuessGame(Cog, name="Guessing Game"):

    def __init__(self, bot: MooseBot):
        self.bot = bot
        self.db = bot.database.db

    async def get_input(self, ctx, datatype, error=''):
        while True:
            try:
                message = await self.bot.client.wait_for('message', check=lambda message: message.author is ctx.author,
                                                         timeout=60)
                message = datatype(message.content)
                return message
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

    @commands.command(help="Guess the number game.")
    async def guess(self, ctx):

        async def play():
            channel = ctx.channel
            await ctx.send("Guess a number between 1 and 100.")
            error = "Please enter a number."
            guess = await self.get_input(ctx, int, error)
            answer = random.randint(1, 100)
            counter = 0

            while guess != answer:
                counter += 1
                if guess > answer:
                    await ctx.send("{} your guess of `{}` is too high! Try again".format(ctx.author.mention, guess))
                    guess = await self.get_input(ctx, int, error)
                else:
                    await ctx.send("{} your guess of `{}` is too low! Try again".format(ctx.author.mention, guess))
                    guess = await self.get_input(ctx, int, error)
            else:
                if counter <= 1:
                    await ctx.send("Congratulations! You got it on the first attempt!")
                else:
                    await ctx.send(f"Congratulations! It took you {counter} tries to guess the correct number.")
                await self.gameover(ctx, play)

        await play()

    @commands.command(help="Rock paper scissors game.")
    async def rps(self, ctx, amount=None):
        user = str(ctx.author.id)
        amount = amount or None
        if amount is None:
            amount = 1
        elif amount == 'all':
            amount = int((await self.db.money.find_one({'userid': user}))['balance'])
        if amount == 'all':
            amount = (await self.db.money.find_one({'userid': user}))['balance']
        if amount <= 0:
            await ctx.send("You need to bet at least 1Ᵽ to play.")

        async def play():
            await ctx.send("Let's play rock, paper, scissors. Select your weapon:")
            choices = ('rock', 'paper', 'scissors')
            computer = choices[random.randint(0, 2)]
            player = await self.get_input(ctx, str)
            player = player.lower()
            if player == 'r':
                player = 'rock'
            elif player == 's':
                player = 'scissors'
            elif player == 'p':
                player = 'paper'
            else:
                player = player

            beats = {'rock': ['paper'],
                     'paper': ['scissors'],
                     'scissors': ['rock']}

            if computer and player in choices:
                if computer == player:
                    await ctx.send(f"**Tie!** You both chose {computer.title()}. You lose no Ᵽlaceholders.")
                    await self.gameover(ctx, play)
                elif player in beats[computer]:
                    await ctx.send(
                        f"**You win!** Moosebot chose: {computer.title()}, and you chose: {player.title()}.You won {amount}Ᵽ.")
                    await self.db.money.update_one({'userid': str(ctx.author.id)}, {'$inc': {'balance': amount}})
                    await self.gameover(ctx, play)
                else:
                    await ctx.send(
                        f"**You lose!** Moosebot chose: {computer.title()}, and you chose: {player.title()}.You lost {amount}Ᵽ.")
                    await self.db.money.update_one({'userid': str(ctx.author.id)}, {'$inc': {'balance': -amount}})
                    await self.gameover(ctx, play)
            else:
                await play()

        await play()


def setup(bot):
    bot.add_cog(GuessGame(bot.moose))
