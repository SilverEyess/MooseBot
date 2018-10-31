from discord.ext import commands


class MemberDisplayName(commands.Converter):
    async def convert(self, ctx, argument):
        try:
            arg = await commands.MemberConverter().convert(ctx, argument)
            return arg.display_name
        except commands.BadArgument:
            return argument
