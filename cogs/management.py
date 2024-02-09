import discord
import sqlite3
from discord.ext import commands

DBFILENAME = "bot.db"

class Management(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    #Commands
    @commands.command(aliases=["purge", "clear"], brief="Cleans messages from channel", description="Clears either 1 or a user set amount of messages from the channel the command was called within.")
    @commands.has_permissions(manage_messages=True)
    async def clean(self, ctx, *, amount=1):
        await ctx.channel.purge(limit=int(amount) + 1)

    @commands.command(brief="Kicks user", description="Removes a specified user from the server. They can re-join if they have an invite link.")
    @commands.has_permissions(kick_members=True)#@commands.has_any_role("Owner", "Moderator")
    async def kick(self, ctx, member : discord.Member, *, reason=None):
        await member.kick(reason=reason)

    @commands.command(brief="Ban user", description="Removes a specified user from the server. They will be unable to re-join until they have been unbanned.")
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member : discord.Member, *, reason=None):
        await member.ban(reason=reason)

    @commands.command(brief="Unban user", description="Removes a specified user from the servers list of banned users. Allowing them to re-join the server with an invite link.")
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, *, member):
        banned_users = await ctx.guild.bans()
        member_name, member_discriminator = member.split("#")
        for ban_entry in banned_users:
            user = ban_entry.user
            if (user.name, user.discriminator) == (member_name, member_discriminator):
                await ctx.guild.unban(user)

    @commands.command(aliases=["a"], brief="Echo messsage", description="The bot will echo the text following the command also deleting the message used to call the commmand.")
    @commands.has_permissions(manage_messages = True)
    async def announcement(self, ctx, *, message=""):
        await ctx.message.channel.purge(limit=1)
        await ctx.send(f"{message}")

    @commands.command(brief="Warn user", description="Sends a warning message with reasoning to the specified user.")
    @commands.has_permissions(manage_messages = True)
    async def warn(self, ctx, member : discord.Member, *, reason=None):
        await ctx.message.channel.purge(limit=1)
        #await member.send(f"**WARNING** from {ctx.message.author.mention}:\n{reason}")
        embed = discord.Embed(title=f"**WARNING** from", description=f"{ctx.message.author.mention}")
        embed.add_field(name="Reason:", value=(f"{reason}"))
        embed.colour = (0xff0000)
        await member.send(content=None, embed=embed)

    @commands.command(brief="User messages", description="Check specified users profanity rating.")
    @commands.has_permissions(manage_messages=True)
    async def messages(self, ctx, member: discord.Member):
        db = sqlite3.connect(DBFILENAME)#Open the database
        cursor = db.cursor()
        cursor.execute("SELECT total FROM users WHERE user=?", (member.id,))#Select mentioned user to see if the value exists
        totalResult = cursor.fetchone()
        totalResult = int(totalResult[0])
        cursor.execute("SELECT profanity FROM users WHERE user=?", (member.id,))#Select mentioned user to see if the value exists
        profanityResult = cursor.fetchone()
        profanityResult = int(profanityResult[0])
        profanityPercent = round((profanityResult / totalResult * 100), 2)
        cursor.execute("SELECT message FROM messages WHERE bool=? AND user=?", (1, member.id))
        messageResult = cursor.fetchall()
        db.close()
        if not messageResult: #if messageResult is empty
            allMessages = "No messages to show"
        else:
            messageResult = messageResult[-5:]#Only select the last 5 messages which contained profanity
            allMessages = ""
            for i in range(0, len(messageResult)):
                allMessages += str(messageResult[i])
            allMessages = allMessages.replace("(", "")
            allMessages = allMessages.replace(")", "")
            allMessages = allMessages.replace(",", " ")
        embed = discord.Embed(title="Messages", description="")
        embed.add_field(name="Total", value=f"{totalResult}")
        embed.add_field(name="Profanity", value=f"{profanityResult}")
        embed.add_field(name="Profanity %", value=f"{profanityPercent}")
        embed.add_field(name="Recent rude messages", value=f"{allMessages}")
        await ctx.send(content=None, embed=embed)

def setup(bot):
    bot.add_cog(Management(bot))
