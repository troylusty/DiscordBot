import discord
import os
from discord.ext import commands

PREFIX = "!"
VERSION = "1.0"

bot = commands.Bot(command_prefix = PREFIX, case_insensitive=True, self_bot = False, description = f"Help Dialog Box")

#Load commands for Cog files
@bot.command(brief="Load specified cog", description="Loads the specified cog from the folder of cogs.")
@commands.is_owner()#@commands.has_role("Owner")
async def load(ctx, extension): #Load command
    bot.load_extension(f"cogs.{extension}")

@bot.command(brief="Unload specified cog", description="Unloads the specified cog from the folder of cogs.")
@commands.is_owner()
async def unload(ctx, extension):#Unload command
    bot.unload_extension(f"cogs.{extension}")

@bot.command(brief="Reload specified cog", description="Unloads and loads the specified cog from the folder of cogs.")
@commands.is_owner()
async def reload(ctx, extension):#Reload command
    bot.unload_extension(f"cogs.{extension}")
    bot.load_extension(f"cogs.{extension}")

#Read all Cog files in.
for filename in os.listdir("./cogs"):
    if filename.endswith(".py"):
        bot.load_extension(f"cogs.{filename[:-3]}")

#Commands
@bot.command(brief="Shows info about the bot", description="Shows info about the bot.")
async def info(ctx):
    embed = discord.Embed(title=f"{bot.user.name}", description=f"Made by **Troy#7760**")
    embed.add_field(name="Version:", value=(f"{VERSION}"))
    embed.add_field(name="Help:", value=(f"Use `{PREFIX} + help` to get started"))
    embed.colour = (0xfb5246)
    #embed.colour = random.randint(0, 0xffffff)#Gives the embed box a random colour everytime.
    embed.set_footer(text="troylusty.com", icon_url="https://pbs.twimg.com/profile_images/1218306285382307841/ur9_dCej_400x400.jpg")
    await ctx.send(content=None, embed=embed)

bot.run("")#Secret token which is unique used to run code on the bot.
