import asyncio
import random
from threading import Lock

import discord
from discord.ext import commands

from moosebot import MooseBot, converters


class Experience:

    def __init__(self, bot: MooseBot):
        self.lock = Lock()
        self.bot = bot
        self.db = bot.database.db

    async def on_message(self, message):
        if message.guild is None:
            return
        else:
            if message.author.bot:
                return
            else:
                await asyncio.gather(self.grantxp(message))

    @commands.command(aliases=['lb'], help='See who has a life the least on your server.')
    async def leaderboard(self, ctx):
        server = str(ctx.guild.id)
        order = 1

        lvls = {}
        async for i in self.db.xp.find_one({'serverid': server}):
            try:
                user = self.bot.client.get_user(int(i))
                lvls[user.id] = await self.db.xp.find_one({'serverid': server})[i]
            except Exception:
                continue
        lvls = sorted(lvls.items(), key=lambda kv: kv[1], reverse=True)
        eligible = []
        for i in lvls:
            try:
                eligible.append(
                    f'▫{order}. '
                    f'**{self.bot.client.get_user(i[0]).display_name}**: '
                    f'{self.db.lvl.find_one({"serverid": server})[str(i[0])] if not None else "0"}'
                    f'`({str(i[1])} exp)` \n'
                )
                order += 1
            except Exception:
                continue

        pagesamount = int(len(eligible) / 10)
        leftover = len(eligible) % 10
        page = 0
        pages = []
        amount1 = 0
        amount2 = 10
        while page < pagesamount:
            pages.append(eligible[amount1:amount2])
            amount1 += 10
            amount2 += 10
            page += 1
        if leftover != 0:
            pages.append(eligible[-leftover:])
            pagesamount += 1
        curpage = 0
        foot_page = 1
        embed = discord.Embed(title="Experience Leaderboard.", description=''.join(pages[curpage]), colour=0xb18dff)
        embed.set_footer(text=f'Page({foot_page}/{pagesamount})')
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
                        embed = discord.Embed(title='Experience Leaderboard.', description=''.join(pages[curpage - 1]),
                                              colour=0xb18dff)
                        embed.set_footer(text=f'Page ({foot_page}/{pagesamount})')
                        await msg.edit(embed=embed)
                        curpage -= 1
                    await msg.remove_reaction(emoji='◀', member=ctx.author)
                elif str(reaction.emoji) == '▶' and user == ctx.author:
                    if curpage == pagesamount - 1:
                        await msg.remove_reaction(emoji='▶', member=ctx.author)
                        continue
                    else:
                        foot_page += 1
                        embed = discord.Embed(title='Experience Leaderboard.', description=''.join(pages[curpage + 1]),
                                              colour=0xb18dff)
                        embed.set_footer(text=f'Page ({foot_page}/{pagesamount})')
                        await msg.edit(embed=embed)
                        curpage += 1
                    await msg.remove_reaction(emoji='▶', member=ctx.author)

    @commands.command(aliases=['lvl', 'rank'], help='Check your current xp and level standings.')
    async def level(self, ctx, member: converters.FullMember = None):
        server = str(ctx.guild.id)
        eligable = {}
        async for i in self.db.lvl.find_one({'serverid': server}):
            try:
                if i == '_id' or i == 'serverid':
                    continue
                else:
                    self.bot.client.get_user(int(i))
                    eligable[i] = await self.db.lvl.find_one({'serverid': server})[i]
            except AttributeError:
                continue
        level_list2 = sorted(eligable.items(), key=lambda kv: kv[1], reverse=True)
        member = member or None
        if member is None:
            user = str(ctx.author.id)
            member = ctx.author
        elif isinstance(member, discord.Member):
            try:
                self.bot.client.get_user(member.id)
                user = str(member.id)

            except AttributeError:
                await ctx.send("That user isn't on this server anymore.")
        else:
            await ctx.send("That isn't a person.")
        rank = [i for i in level_list2 if i[0] == user]
        nextlvl = f'{user}_nextlevel'
        try:
            person = await self.db.xp.find_one({'serverid': server})[user]
            nextlevel = await self.db.xp.find_one({'serverid': server})[nextlvl]
            xp = f"{person}/{nextlevel}"
        except KeyError:
            xp = await self.db.xp.find_one({'serverid': server})[user]
        level = await self.db.lvl.find_one({'serverid': server})[user]
        embed = discord.Embed(title=f"{member.display_name}'s level details",
                              description=f"**Rank:** {level_list2.index(rank[0]) + 1} \n**Level:** {level}\n**Experience:** {xp}",
                              colour=0xb18dff)
        await ctx.send(embed=embed)

    @commands.command(aliases=['gvxp'], help='Bot author only command.')
    @commands.check(MooseBot.is_owner)
    async def givexp(self, ctx, user: converters.FullMember = None, *, args: int):
        user = user or None
        args = args or None
        if user is None:
            await ctx.send("Please tell me who to give xp to.")
        elif args is None:
            await ctx.send(f"Please tell me how much xp to give to `{user.display_name}`.")
        else:
            await self.db.xp.update_one({'serverid': str(ctx.guild.id)}, {'$inc': {str(user.id): args}})
            await ctx.send(f"{args} xp successfully given to {user.display_name}.")

    @commands.command(aliases=['rmvxp'], help='Bot author only command.')
    @commands.check(MooseBot.is_owner)
    async def removexp(self, ctx, user: converters.FullMember = None, *, args):
        user = user or None
        args = args or None
        if user is None:
            await ctx.send("Please tell me who to take xp from.")
        elif args is None:
            await ctx.send(f"Please tell me how much xp to take from `{user.display_name}`.")
        else:
            if args == 'all' or args == '*':
                beforexp = await self.db.xp.find_one({'userid': str(user.id)})
                if beforexp is None:
                    await ctx.send("This user had no xp to take...")
                else:
                    await self.db.xp.update_one({'userid': str(user.id)}, {'$set': {'experience': 0}})
                    await ctx.send(f"{beforexp} xp successfully taken from {user.display_name}.")
            else:
                await self.db.xp.update_one({'userid': str(user.id)}, {'$inc': {'experience': -int(args)}})
                await ctx.send(f"{args} xp successfully taken from {user.display_name}.")

    async def grantxp(self, message):
        self.lock.acquire()
        xpamount = random.randint(1, 10)
        try:
            author = str(message.author.id)
            await self.db.xp.update_one({'serverid': str(message.guild.id)}, {'$inc': {author: xpamount}}, True)
            userxp = await self.db.xp.find_one({'serverid': str(message.guild.id)})
            userxp = userxp[author]
            if userxp is not None:
                level_amount = 100
                newlevel = 0
                levelxp = 0
                while levelxp < userxp:
                    if newlevel < 50:
                        level_amount = int(level_amount * 0.04) + level_amount
                    else:
                        level_amount = level_amount
                    levelxp += int(level_amount)
                    newlevel += 1
                    if levelxp > userxp:
                        newlevel -= 1
                userlvl = await self.db.lvl.find_one({'serverid': str(message.guild.id)})
                userlvl = userlvl[author]
                await self.db.xp.update_one({'serverid': str(message.guild.id)}, {
                    '$set': {f'{author}_nextlevel': levelxp + (int((level_amount * 0.04) + level_amount))}}, True)
                if author not in await self.db.lvl.find_one({'serverid': str(message.guild.id)}):
                    await self.db.lvl.update_one({'serverid': str(message.guild.id)}, {'$set': {author: newlevel}},
                                                 True)
                elif newlevel != userlvl:
                    await message.channel.send(
                        f"Congratulations {message.author.mention} you leveled up to level {newlevel}!")
                    await self.db.lvl.update_one({'serverid': str(message.guild.id)}, {'$set': {author: newlevel}},
                                                 True)
        finally:
            self.lock.release()
