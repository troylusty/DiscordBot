import discord
import os
import youtube_dl
from discord.ext import commands
from discord.utils import get

players = {}

class Audio(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["j"], brief="Bot joins the channel", description="Bot joins the channel the message authour is currently in.")
    async def join(self, ctx):
        global voice
        channel = ctx.message.author.voice.channel
        voice = get(self.bot.voice_clients, guild=ctx.guild)
        if voice and voice.is_connected():
            await voice.move_to(channel)
        else:
            voice = await channel.connect()
        await ctx.send(f"joined {channel}")

    @commands.command(aliases=["l"], brief="Bot leaves the channel", description="Bot leaves the channel.")
    async def leave(self, ctx):
        channel = ctx.message.author.voice.channel
        voice = get(self.bot.voice_clients, guild=ctx.guild)
        if voice and voice.is_connected():
            await voice.disconnect()
            await ctx.send(f"left {channel}")
        else:
            await ctx.send(f"not in any voice channel")

    @commands.command(aliases=["p", "pla"], brief="Play audio from YouTube video.", description="Play audio from specified YouTube video.")
    async def play(self, ctx, url : str):
        song_there = os.path.isfile("song.mp3")
        try:
            if song_there:
                os.remove("song.mp3")
                print("removed old song file")
        except PermissionError:
            print("tried to delete old song file")
            await ctx.send(f"error music playing")
            return
        await ctx.send(f"getting ready")
        voice = get(self.bot.voice_clients, guild=ctx.guild)
        ydl_opts = {
            'format': 'bestaudio/best',
            'quiet': True,
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            print(f"downloading audio")
            ydl.download([url])
        for file in os.listdir("./"):
            if file.endswith(".mp3"):
                name = file
                print(f"renamed audio file {file}")
                os.rename(file, "song.mp3")
        voice.play(discord.FFmpegPCMAudio("song.mp3"), after=lambda e: print(f"{name} has finished playing"))#If song is done do function `e`.
        voice.source = discord.PCMVolumeTransformer(voice.source)
        voice.source.volume = 0.33
        nnname = name.rsplit("-", 2)
        await ctx.send(f"playing {nnname[0]}")
        print("playing")
        """
        https://youtu.be/Bp9SZYqIWIM
        """

    @commands.command(aliases=["pau"], brief="Pause song", description="Pause currently playing song.")
    async def pause(self, ctx):
        voice = get(self.bot.voice_clients, guild=ctx.guild)
        if voice and voice.is_playing():
            print(f"music paused")
            voice.pause()
            await ctx.send(f"music paused")
        else:
            print("music not playing")
            await ctx.send("music not playing failed to pause")

    @commands.command(aliases=["r"], brief="Resume song", description="Resume paused song.")
    async def resume(self, ctx):
        voice = get(self.bot.voice_clients, guild=ctx.guild)
        if voice and voice.is_paused():
            print(f"music resumed")
            voice.resume()
            await ctx.send(f"music resumed")
        else:
            print("music not paused")
            await ctx.send("music not paused")

    @commands.command(aliases=["s"], brief="Stop playing all songs", description="Stop playing all songs and clear queues.")
    async def stop(self, ctx):
        voice = get(self.bot.voice_clients, guild=ctx.guild)
        if voice and voice.is_playing():
            print(f"music stopped")
            voice.stop()
            await ctx.send(f"music stopped")
        else:
            print("music not playing failed to stop")
            await ctx.send("music not playing failed to stop")

def setup(bot):
    bot.add_cog(Audio(bot))