from discord.ext import commands


class VoiceChannel(commands.Converter):

    async def convert(self, ctx, argument):
        try:
            arg = await commands.VoiceChannelConverter().convert(ctx, argument)
            return arg
        except commands.BadArgument:
            arg = [i for i in ctx.guild.voice_channels if
                   i.name.lower() == argument.lower()]
            if len(arg) >= 1:
                return arg[0]
            else:
                arg = [i for i in ctx.guild.voice_channels if
                       i.name.lower().startswith(argument.lower())]
                if len(arg) >= 1:
                    return arg[0]
                else:
                    return argument
