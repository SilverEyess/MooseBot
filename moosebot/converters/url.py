from discord.ext import commands


class Url(commands.Converter):

    async def convert(self, ctx, arg):
        if arg.startswith("www."):
            arg = "https://" + arg
            return arg
        elif not arg.startswith("http://www."):
            arg = "http://www." + arg
            if not arg.endswith(".com") and not arg.endswith(".net") and not arg.endswith(".org"):
                arg = arg + ".com"
                return arg
            else:
                return arg
        elif not arg.endswith(".com") and not arg.endswith(".net") and not arg.endswith(".org"):
            arg = arg + ".com"
            return arg
