import datetime
import discord
import os
import sqlite3
from discord.ext import commands
from profanity_check import predict

DBFILENAME = "bot.db"

def createDB():
    if os.path.isfile(DBFILENAME):
        db = sqlite3.connect(DBFILENAME)
    else:
        db = sqlite3.connect(DBFILENAME)
        print(f"File didn't exist. Created file: {DBFILENAME}")
        cursor = db.cursor()
        cursor.execute("CREATE TABLE if not exists guilds (id INTEGER, prefix TEXT, PRIMARY KEY (id))")
        cursor.execute("CREATE TABLE if not exists messages (date TEXT, time TEXT, message TEXT, details TEXT, user INTEGER, guild INTEGER, link TEXT, bool INTEGER, PRIMARY KEY (date, time), FOREIGN KEY (user) REFERENCES users (user), FOREIGN KEY (guild) REFERENCES guilds (id))")
        cursor.execute("CREATE TABLE if not exists users (user INTEGER, username TEXT, total INTEGER, profanity INTEGER, PRIMARY KEY (user))")
        db.commit()
    db.close()

class Listeners(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        try:
            createDB()#Run createDB. This will check for the database and tables. If they don't exist they will be created.
            print(f"Bot is ready (createDB successful)")
            print(f"Name: {self.bot.user.name}\nID: {self.bot.user.id}")  # Prints the bots username (e.g. Bot#1111) and prints out the user id of the bot (e.g. 58492482649273613).
            await self.bot.change_presence(status=discord.Status.dnd, activity=discord.Activity(type=discord.ActivityType.watching, name=f"in {len(self.bot.guilds)} guild(s) with {len(set(self.bot.get_all_members()))} members"))
        except:
            print(f"Bot is ready (createDB failed)")
            print (f"Name: {self.bot.user.name}\nID: {self.bot.user.id}")#Prints the bots username (e.g. Bot#1111) and prints out the user id of the bot (e.g. 58492482649273613).
            await self.bot.change_presence(status=discord.Status.dnd, activity=discord.Activity(type=discord.ActivityType.watching, name=f"in {len(self.bot.guilds)} guild(s) with {len(set(self.bot.get_all_members()))} members"))

    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = member.guild.system_channel
        if channel is not None:
            await channel.send(f"Hey {member.mention} :wave:")

    @commands.Cog.listener()
    async def on_member_remove(self, guild):
        channel = member.guild.system_channel
        if channel is not None:
            await channel.send(f"Bye {member.mention} :cry:")

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return
        else:
            messageLink = f"https://discordapp.com/channels/{message.guild.id}/{message.channel.id}/{message.id}"
            if message.content != "":  # Checks if the message contains content. (Stops server messages being registered)
                db = sqlite3.connect(DBFILENAME)  # Add guild to guilds table
                cursor = db.cursor()
                cursor.execute("SELECT id FROM guilds WHERE id=?", (message.guild.id,))
                guildResult = cursor.fetchone()
                if guildResult:
                    # Does exist
                    db.close()
                else:
                    # Doesn't exist
                    cursor.execute("INSERT INTO guilds(id, prefix) VALUES(?,?)", (message.guild.id, "!"))
                    db.commit()
                    db.close()
                db = sqlite3.connect(DBFILENAME)#Open the database
                cursor = db.cursor()
                cursor.execute("SELECT user FROM users WHERE user=?", (message.author.id,))#Select `user` to see if the value exists
                userResult = cursor.fetchone()
                if userResult:
                    #User does exist
                    cursor.execute("SELECT total FROM users WHERE user=?", (message.author.id,))#Select the total from the user
                    totalResult = cursor.fetchone()
                    totalResult = int(totalResult[0])
                    totalResult += 1#Add 1 to the total (messages) count
                    if predict([f"{message.content}"]) == [1]:#If message contains profanity [1] will be returned
                        cursor.execute("SELECT profanity FROM users WHERE user=?", (message.author.id,))#Select the total profanity from the user
                        totalProfanity = cursor.fetchone()
                        totalProfanity = int(totalProfanity[0])
                        totalProfanity += 1#Add 1 to the total profanity count
                        cursor.execute("UPDATE users SET profanity=? WHERE user=?", (totalProfanity, message.author.id))
                        cursor.execute("UPDATE users SET total=? WHERE user=?", (totalResult, message.author.id))#Add the new total value into the table
                        cursor.execute("UPDATE users SET username=? WHERE user=?", (message.author.name, message.author.id))
                        dateTime = datetime.datetime.now()
                        time = str(dateTime.strftime("%X")) + ":" + str((dateTime.strftime("%f")))
                        cursor.execute("INSERT INTO messages(date, time, message, details, user, guild, link, bool) VALUES(?,?,?,?,?,?,?,?)", (str(dateTime.strftime("%x")), (time), str(message.content), str(message), int(message.author.id), int(message.guild.id), str(messageLink), int(1)))
                    else:
                        cursor.execute("UPDATE users SET total=? WHERE user=?", (totalResult, message.author.id))#Add the new total value into the table
                        cursor.execute("UPDATE users SET username=? WHERE user=?", (message.author.name, message.author.id))
                        dateTime = datetime.datetime.now()
                        time = str(dateTime.strftime("%X")) + ":" + str((dateTime.strftime("%f")))
                        cursor.execute("INSERT INTO messages(date, time, message, details, user, guild, link, bool) VALUES(?,?,?,?,?,?,?,?)", (str(dateTime.strftime("%x")), (time), str(message.content), str(message), int(message.author.id), int(message.guild.id), str(messageLink), int(0)))
                    db.commit()
                else:
                    #User doesn't exist
                    if predict([f"{message.content}"]) == [1]:#If message contains profanity [1] will be returned
                        cursor.execute("INSERT INTO users(user, username, total, profanity) VALUES(?,?,?,?)", (message.author.id, message.author.name, 1, 1))#Adds the user into the table and adds a value of 1 as the total
                        dateTime = datetime.datetime.now()
                        time = str(dateTime.strftime("%X")) + ":" + str((dateTime.strftime("%f")))
                        cursor.execute("INSERT INTO messages(date, time, message, details, user, guild, link, bool) VALUES(?,?,?,?,?,?,?,?)", (str(dateTime.strftime("%x")), (time), str(message.content), str(message), int(message.author.id), int(message.guild.id), str(messageLink), int(0)))
                    else:
                        cursor.execute("INSERT INTO users(user, username, total, profanity) VALUES(?,?,?,?)", (message.author.id, message.author.name, 1, 0))#Adds the user into the table and adds a value of 1 as the total
                        dateTime = datetime.datetime.now()
                        time = str(dateTime.strftime("%X")) + ":" + str((dateTime.strftime("%f")))
                        cursor.execute("INSERT INTO messages(date, time, message, details, user, guild, link, bool) VALUES(?,?,?,?,?,?,?,?)", (str(dateTime.strftime("%x")), (time), str(message.content), str(message), int(message.author.id), int(message.guild.id), str(messageLink), int(0)))
                    db.commit()
                    db.close()
                #await self.bot.process_commands(message)
            else:
                return

def setup(bot):
    bot.add_cog(Listeners(bot))
