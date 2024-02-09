import random
from discord.ext import commands

class Default(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["flip"], brief="Flips a coin", description="Generates a random number between 0 and 1. If 0 is generated Heads is returned and if 1 is generated Tails is returned.")
    async def coin(self, ctx):
        zeroOrOne = random.randint(0,1)
        if zeroOrOne == 0:
            result = "Heads"
        else:
            result = "Tails"
        await ctx.send(f"It's {result}")

    @commands.command(aliases=["roll"], brief="Rolls a dice", description="Generates a random number between 1 and 6 then returns the value.")
    async def dice(self, ctx):
        roll = random.randint(1, 6)#Generate a random number between 1 and 6.
        await ctx.send(f"I've rolled a {roll} :game_die:")#Used an f-string to easily format the string since it makes it easier to add more variables and other values.

    @commands.command(aliases=["ping"], brief="Displays the bot's latency", description="Uses bot.latency to display the latency of the bot.")
    async def latency(self, ctx):
        await ctx.send(f"{round(self.bot.latency * 1000)}ms :alarm_clock:")

def setup(bot):
    bot.add_cog(Default(bot))
