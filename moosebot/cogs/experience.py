import asyncio
import random
from threading import Lock

import discord
from discord.ext import commands
from discord.ext.commands import Cog
import pymongo

from moosebot import MooseBot, converters


class Experience(Cog):

    def __init__(self, bot: MooseBot):
        self.lock = Lock()
        self.bot = bot
        self.db = bot.database.db

    @Cog.listener()
    async def on_message(self, message):
        if message.guild is None:
            return
        else:
            if message.author.bot:
                return
            elif message.content.startswith('>') or message.content.startswith('$'):
                return
            else:
                await asyncio.gather(self.grantxp(message))

    @commands.command(aliases=['lb'], help='See who has a life the least on your server.')
    async def leaderboard(self, ctx):
        server = str(ctx.guild.id)
        desc = ""

        people = self.db.money.find()
        # people.sort({'xp': server})
        rank = 1
        # print(people)
        for i in await people.to_list(length=20):
            # print(i)
            if 'xp' in i:
                if str(ctx.guild.id) in i['xp']:
                    # print('server')
                    user = self.bot.client.get_user(int(i["userid"]))
                    if user is None:
                        pass
                    else:
                        if not user.bot:
                            desc += f'{rank}. {user.display_name}: {i["xp"][server]["xp"]}\n'
                            rank += 1

        embed = discord.Embed(title='Experience Leaderboard', description=desc)
        await ctx.send(embed=embed)

    @commands.command(aliases=['lvl', 'rank'], help='Check your current xp and level standings.')
    async def level(self, ctx, member: converters.FullMember = None):
        member = member or ctx.author
        server = str(ctx.guild.id)
        if not isinstance(member, discord.Member):
            return
        else:
            desc = ""
            person = await self.db.money.find_one({'userid': str(member.id)})
            if 'xp' not in person:
                await ctx.send('This person has not earned any xp yet.')
            elif server not in person['xp']:
                await ctx.send('This person has not earned any xp yet.')
            elif 'xp' not in person['xp'][server]:
                await ctx.send('This person has not earned any xp yet.')
            else:
                memberxp = person['xp'][server]['xp']
                if 'lvl' not in person['xp'][server]:
                    memberlvl = 0
                else:
                    memberlvl = person['xp'][server]['lvl']
                if 'nxtlvl' not in person['xp'][server]:
                    membernxt = 104
                else:
                    membernxt = person['xp'][server]['nxtlvl']
                desc += f"**💠 Level:** {memberlvl}\n**💠 Exp:** {memberxp}\n**💠 Exp for next level:** {membernxt}"

                embed = discord.Embed(title=f"{member.display_name}'s experience info.", description=desc, colour=0xb18dff)
                embed.set_thumbnail(url=member.avatar_url_as(format='png'))
                await ctx.send(embed=embed)

    @commands.command(aliases=['gvxp'], help='Bot author only command.', Hidden=True)
    @commands.check(MooseBot.is_owner)
    async def givexp(self, ctx, amount: int, *, user: converters.FullMember = None):
        user = user or None
        amount = amount or None
        server = str(ctx.guild.id)
        if user is None:
            await ctx.send("Please tell me who to give xp to.")
        elif amount is None:
            await ctx.send(f"Please tell me how much xp to give to `{user.display_name}`.")
        elif amount <= 0:
            await ctx.send('You cannot give negative xp.')
        else:
            await self.db.money.update_one({'userid': str(user.id)}, {'$inc': {f'xp.{server}.xp': amount}})
            await ctx.send(f"{amount} xp successfully given to {user.display_name}.")

    @commands.command(aliases=['rmvxp'], help='Bot author only command.')
    @commands.check(MooseBot.is_owner)
    async def removexp(self, ctx, amount: int, *, user: converters.FullMember = None):
        user = user or None
        amount = amount or None
        if user is None:
            await ctx.send("Please tell me who to take xp from.")
        elif amount is None:
            await ctx.send(f"Please tell me how much xp to take from `{user.display_name}`.")
        elif amount <= 0:
            await ctx.send('You need to specify a positive number')
        else:
            server = str(ctx.guild.id)
            if amount == 'all' or amount == '*':
                xplist = await self.db.money.find_one({'userid': str(user.id)})
                beforexp = xplist['xp'][server]['xp']
                if beforexp is None:
                    await ctx.send("This user had no xp to take...")
                else:
                    await self.db.money.update_one({'userid': str(user.id)}, {f'$inc': {'xp.{server}.xp': 0}})
                    await ctx.send(f"{beforexp} xp successfully taken from {user.display_name}.")
            else:
                await self.db.money.update_one({'userid': str(user.id)}, {'$inc': {f'xp.{server}.xp': -int(amount)}})
                await ctx.send(f"{amount} xp successfully taken from {user.display_name}.")

    async def grantxp(self, message):
        # self.lock.acquire()
        xpamount = random.randint(1, 10)
        # try:
        author = str(message.author.id)
        if message.author.bot:
            return
        else:
            server = str(message.guild.id)
            await self.db.money.update_one({'userid': author}, {'$inc': {f'xp.{server}.xp': xpamount}})
            userlist = await self.db.money.find_one({'userid': author})
            if userlist is not None:
                try:
                    userxp = userlist['xp'][server]['xp']
                except Exception:
                    userxp = 0
            else:
                userxp = 0
            if userxp is not 0:
                level_amount = 400
                newlevel = 0
                levelxp = 0
                while levelxp < userxp:
                    nextlvl = int(level_amount * 1.04)
                    level_amount += (nextlvl - level_amount)
                    levelxp += level_amount
                    newlevel += 1
                    if levelxp > userxp:
                        newlevel -= 1
                userlvl = await self.db.money.find_one({'userid': author})
                if server not in userlvl['xp']:
                    userlvl = 0
                elif 'lvl' not in userlvl['xp'][server]:
                    userlvl = 0
                else:
                    userlvl = userlvl['xp'][server]['lvl']
                await self.db.money.update_one({'userid': author}, {'$set': {f'xp.{server}.nxtlvl': levelxp}}, True)
                if userlvl is None:
                    await self.db.money.update_one({'userid': author}, {'$set': {f'xp.{server}.lvl': newlevel}}, True)
                elif newlevel != userlvl:
                    await message.channel.send(f"Congratulations {message.author.mention} you leveled up to level {newlevel}!")
                    await self.db.money.update_one({'userid': author}, {'$set': {f'xp.{server}.lvl': newlevel}}, True)
                    return
        # except Exception:
        #     self.lock.release()
        # finally:
        #     self.lock.release()

    # async def test(self, ctx):
    #     for i in self.db.lvl:
    #         for x in i:
    #             if x != 'serverid':
    #                 


def setup(bot):
    bot.add_cog(Experience(bot.moose))
