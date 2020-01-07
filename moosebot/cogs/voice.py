import discord
import youtube_dl
from discord.ext import commands
from discord.ext.commands import Cog

from moosebot import MooseBot


class Voice(Cog):

    def __init__(self, bot: MooseBot):
        self.bot = bot

    @commands.command()
    async def testp(self, ctx, url):
        voice_channel = ctx.author.voice.channel
        opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192'
            }]
        }

        # Check that user is in voice channel
        if ctx.author.voice.channel is not None:

            # Check if already a voice client
            if ctx.guild.voice_client is not None:
                # if there is, add song to queue
                pass

            # if there isn't create one
            elif ctx.guild.voice_client is None:
                # join VC
                vc = await voice_channel.connect(timeout=60, reconnect=True)
            # Check that is valid url
            if url.startswith("https://www.youtube.com/watch?v="):

                # Get video information and store in song_info, with video source as url
                with youtube_dl.YoutubeDL(opts) as ydl:
                    song_info = ydl.extract_info(url, download=False)
                    url = song_info['url']
                    # play audio

                vc.play(discord.FFmpegPCMAudio(url))
                embed = discord.Embed(title="Now playing", description="[{}]({}) [{}]".format(song_info['title'], url,
                                                                                              ctx.author.mention))
                await ctx.send(embed=embed)

                # display now playing

            # If not, ask for valid url
            else:
                await ctx.send("Please enter a valid Youtube URL.")

        # If not in a voice channel, ask user to join one
        else:
            await ctx.send("Please join a voice channel")

    @commands.command(help="Gets me to join your voice channel.")
    async def join(self, ctx):
        voice_channel = ctx.author.voice.channel
        await voice_channel.connect()

    @commands.command(help="Gets me to leave your voice channel.")
    async def leave(self, ctx):
        for x in self.bot.client.voice_clients:
            if x.guild == ctx.message.guild:
                return await x.disconnect()

        return await ctx.send("\u200BI am not connected to any voice channel on this server!")


def setup(bot):
    bot.add_cog(Voice(bot.moose))
