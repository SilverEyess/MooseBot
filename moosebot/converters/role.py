from discord.ext import commands


class Role(commands.Converter):
    async def convert(self, ctx, arg):
        try:
            arg = await commands.RoleConverter().convert(ctx, arg)
            return arg
        except commands.BadArgument:
            arg = arg.lower()
            role = [x for x in ctx.guild.roles if x.name.lower() == arg or x.name.lower().startswith(arg)]
            if len(role) == 0:
                await ctx.send(f"There is no role `{arg}`.")
            else:
                return role[0]
