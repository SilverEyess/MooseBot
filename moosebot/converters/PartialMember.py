import discord
from discord.ext import commands


class PartialMember(commands.Converter):
    async def convert(self, ctx, argument):
        if len(argument) == 1 and not isinstance(argument, discord.Member):
            return argument
        else:
            try:
                arg = await commands.MemberConverter().convert(ctx, argument)
                return arg
            except commands.BadArgument:
                arg = [i for i in ctx.guild.members if
                       i.name.lower() == argument.lower() or i.display_name.lower() == argument.lower()]
                if len(arg) >= 1:
                    return arg[0]
                else:
                    arg = [i for i in ctx.guild.members if
                           i.name.lower().startswith(argument.lower()) or i.display_name.lower().startswith(
                               argument.lower())]
                    if len(arg) >= 1:
                        return arg[0]
                    else:
                        return argument