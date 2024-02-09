import discord
import json
import time
import urllib.request
from discord.ext import commands

logins = {
    "steam": {
        "api-key": "",
    },
    "riot": {
        "api-key": "",
    }
}


def most_frequent(List):
    counter = 0
    num = List[0]
    for i in List:
        curr_frequency = List.count(i)
        if (curr_frequency > counter):
            counter = curr_frequency
            num = i
    return num


class Integrations(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(brief="Steam user's ban info", description="Uses the Steam API to return a specified users detailed ban status.")
    async def steambans(self, ctx, *, steamID64=""):
        steamWebApiKey = logins["steam"]["api-key"]
        try:
            with urllib.request.urlopen(
                    f"http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key={steamWebApiKey}&steamids={steamID64}") as url:
                playerSummaries = json.loads(url.read().decode())
            try:
                personaname = playerSummaries['response']['players'][0]['personaname']
            except:
                personaname = "*data not found*"
            try:
                realname = playerSummaries['response']['players'][0]['realname']
            except:
                realname = "*data not found*"
            try:
                avatarfull = playerSummaries['response']['players'][0]['avatarfull']
            except:
                avatarfull = "https://steamcdn-a.akamaihd.net/steamcommunity/public/images/avatars/b5/b5bd56c1aa4644a474a2e4972be27ef9e82e517e_full.jpg"
            try:
                profileurl = playerSummaries['response']['players'][0]['profileurl']
            except:
                profileurl = f"https://steamcommunity.com/profiles/{steamID64}"
        except:
            personaname, realname, avatarfull, profileurl = "*data not loaded*", "*data not loaded*", "https://steamcdn-a.akamaihd.net/steamcommunity/public/images/avatars/b5/b5bd56c1aa4644a474a2e4972be27ef9e82e517e_full.jpg", f"https://steamcommunity.com/profiles/{steamID64}"
        try:
            with urllib.request.urlopen(
                    f"http://api.steampowered.com/ISteamUser/GetPlayerBans/v1/?key={steamWebApiKey}&steamids={steamID64}") as url:
                getPlayerBans = json.loads(url.read().decode())
            try:
                communityBanned = getPlayerBans['players'][0]['CommunityBanned']
            except:
                communityBanned = "*data not found*"
            try:
                vacBanned = getPlayerBans['players'][0]['VACBanned']
            except:
                vacBanned = "*data not found*"
            try:
                numberOfVACBans = getPlayerBans['players'][0]['NumberOfVACBans']
            except:
                numberOfVACBans = "*data not found*"
            try:
                daysSinceLastBan = getPlayerBans['players'][0]['DaysSinceLastBan']
            except:
                daysSinceLastBan = "*data not found*"
            try:
                numberOfGameBans = getPlayerBans['players'][0]['NumberOfGameBans']
            except:
                numberOfGameBans = "*data not found*"
            try:
                economyBan = getPlayerBans['players'][0]['EconomyBan']
            except:
                economyBan = "*data not found*"
        except:
            communityBanned, vacBanned, numberOfVACBans, daysSinceLastBan, numberOfGameBans, economyBan = "*data not loaded*", "*data not loaded*", "*data not loaded*", "*data not loaded*", "*data not loaded*", "*data not loaded*"
        embed = discord.Embed(title="Steam Bans Check", description="")
        embed.set_image(url=f"{avatarfull}")
        embed.add_field(name="Username", value=f"{personaname}")
        embed.add_field(name="Real name", value=f"{realname}")
        embed.add_field(name="Profile url", value=f"{profileurl}")
        embed.add_field(name="VAC", value=f"{vacBanned}")
        embed.add_field(name="Number of VAC bans", value=f"{numberOfVACBans}")
        embed.add_field(name="Days since last ban", value=f"{daysSinceLastBan}")
        embed.add_field(name="Number of game bans", value=f"{numberOfGameBans}")
        embed.add_field(name="Community banned", value=f"{communityBanned}")
        embed.add_field(name="Economy ban", value=f"{economyBan}")
        embed.colour = (0x5dcff6)
        embed.set_footer(text="Steam",
                         icon_url="https://upload.wikimedia.org/wikipedia/commons/thumb/8/83/Steam_icon_logo.svg/2000px-Steam_icon_logo.svg.png")
        await ctx.send(content=None, embed=embed)

    @commands.command(aliases=["csgo", "cs"], brief="CS:GO stats info", description="Uses the Steam API to return and calculate a specified users Counter-Strike: Global Offensive statistics.")
    async def csgostats(self, ctx, *, steamID64=""):
        steamWebApiKey = logins["steam"]["api-key"]
        try:
            with urllib.request.urlopen(f"http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key={steamWebApiKey}&steamids={steamID64}") as url:
                playerSummaries = json.loads(url.read().decode())
            try:
                personaname = playerSummaries['response']['players'][0]['personaname']
            except:
                personaname = "*data not found*"
            try:
                realname = playerSummaries['response']['players'][0]['realname']
            except:
                realname = "*data not found*"
            try:
                avatarfull = playerSummaries['response']['players'][0]['avatarfull']
            except:
                avatarfull = "*data not found*"
            try:
                profileurl = playerSummaries['response']['players'][0]['profileurl']
            except:
                profileurl = "*data not found*"
        except:
            personaname, realname, avatarfull, profileurl = "*data not loaded*", "*data not loaded*", "https://steamcdn-a.akamaihd.net/steamcommunity/public/images/avatars/b5/b5bd56c1aa4644a474a2e4972be27ef9e82e517e_full.jpg", f"https://steamcommunity.com/profiles/{steamID64}"
        try:
            with urllib.request.urlopen(f"http://api.steampowered.com/ISteamUserStats/GetUserStatsForGame/v0002/?appid=730&key={steamWebApiKey}&steamid={steamID64}") as url:
                getUserStatsForGame = json.loads(url.read().decode())
            playerstats = getUserStatsForGame["playerstats"]
            stats = playerstats["stats"]
            for i in range(len(stats)):
                if stats[i]['name'] == "total_kills":
                    totalKills = stats[i]['value']
                if stats[i]['name'] == "total_deaths":
                    totalDeaths = stats[i]['value']
                if stats[i]['name'] == "total_time_played":
                    totalTimePlayed = stats[i]['value']
                if stats[i]['name'] == "total_wins":
                    totalWins = stats[i]['value']
                if stats[i]['name'] == "total_kills_headshot":
                    totalKillsHeadshot = stats[i]['value']
                if stats[i]['name'] == "total_shots_fired":
                    totalShotsFired = stats[i]['value']
                if stats[i]['name'] == "total_shots_hit":
                    totalShotsHit = stats[i]['value']
                if stats[i]['name'] == "total_mvps":
                    totalMvps = stats[i]['value']
            killToDeath = round((totalKills / totalDeaths), 2)
            accuracy = round((totalShotsHit / totalShotsFired * 100), 2)
            headshotPercentage = round((totalKillsHeadshot / totalKills * 100), 2)
            totalTimePlayed = round(totalTimePlayed / 3600)
        except:
            killToDeath, totalKills, totalTimePlayed, accuracy, headshotPercentage, totalMvps = "*data not loaded*", "*data not loaded*", "*data not loaded*", "*data not loaded*", "*data not loaded*", "*data not loaded*"
        try:
            data = {}
            for i in range(len(stats)):
                if stats[i]['name'].startswith("total_kills_"):
                    data[f"{stats[i]['name']}"] = int(f"{stats[i]['value']}")
            try:
                data.pop("total_kills_knife")
            except:
                error = True
            try:
                data.pop("total_kills_hegrenade")
            except:
                error = True
            try:
                data.pop("total_kills_headshot")
            except:
                error = True
            try:
                data.pop("total_kills_enemy_weapon")
            except:
                error = True
            try:
                data.pop("total_kills_enemy_blinded")
            except:
                error = True
            try:
                data.pop("total_kills_knife_fight")
            except:
                error = True
            try:
                data.pop("total_kills_against_zoomed_sniper")
            except:
                error = True
            try:
                data.pop("total_kills_molotov")
            except:
                error = True
            try:
                data.pop("total_kills_taser")
            except:
                error = True
            data = {k: v for k, v in sorted(data.items(), key=lambda item: item[1], reverse=True)} # Sort weapons into most used
            dict_items = data.items()
            values = list(dict_items)[:5] # Cut to the top 5 most used
            for i in range(0, len(values)): # Save stats to easily referenceable variables
                if i == 0:
                    ak47 = values[i][1]
                elif i == 1:
                    awp = values[i][1]
                elif i == 2:
                    m4a1 = values[i][1]
                elif i == 3:
                    deagle = values[i][1]
                elif i == 4:
                    hkp2000 = values[i][1]
        except:
            error = True
        if error == True:
            print(f"error is true")
        try:
            with urllib.request.urlopen(
                    f"http://api.steampowered.com/ISteamUser/GetPlayerBans/v1/?key={steamWebApiKey}&steamids={steamID64}") as url:
                getPlayerBans = json.loads(url.read().decode())
            try:
                vacBanned = getPlayerBans['players'][0]['VACBanned']
            except:
                vacBanned = "*data not found*"
        except:
            vacBanned = "*data not loaded*"
        embed = discord.Embed(title="CS:GO Stats", description="")
        embed.set_image(url=f"{avatarfull}")
        embed.add_field(name="Username", value=f"{personaname}")
        embed.add_field(name="Real name", value=f"{realname}")
        embed.add_field(name="Profile url", value=f"{profileurl}")
        embed.add_field(name="VAC", value=f"{vacBanned}")
        embed.add_field(name="K/D", value=f"{killToDeath}")
        embed.add_field(name="Total Kills", value=f"{totalKills}")
        embed.add_field(name="Time Played", value=f"{totalTimePlayed} hours")
        #embed.add_field(name="Win Percentage", value=f"")
        embed.add_field(name="Accuracy", value=f"{accuracy}%")
        embed.add_field(name="Headshot Percentage", value=f"{headshotPercentage}%")
        embed.add_field(name="MVPs", value=f"{totalMvps}")
        embed.add_field(name="Total Weapon Kills", value=f"AK-47: {ak47}, M4A1: {m4a1}, AWP: {awp}, DEAGLE: {deagle}, HKP2000: {hkp2000}")
        embed.colour = (0xf99d1c)
        embed.set_footer(text="Counter-Strike: Global Offensive", icon_url="http://i.imgur.com/JP5mOFP.png")
        await ctx.send(content=None, embed=embed)

    @commands.command(brief="UNFINISHED - League of Legends Stats", description="League of Legends Stats")
    async def lol(self, ctx, name, region="DEFAULT"):
        print(region.casefold())
        start = time.time()
        riotGamesApiKey = logins["riot"]["api-key"]
        regions = ["BR1", "EUN1", "EUW1", "JP1", "KR", "LA1", "LA2", "NA1", "OC1", "TR1", "RU"]
        if region == "DEFAULT":
            for i in range(0, len(regions)):
                try:
                    with urllib.request.urlopen(
                            f"https://{regions[i].casefold()}.api.riotgames.com/lol/summoner/v4/summoners/by-name/{name.casefold()}?api_key={riotGamesApiKey}") as url:
                        data = json.loads(url.read().decode())
                        print(f"FOUND {regions[i]}")
                        correctRegion = regions[i].casefold()
                        if data == None:
                            break  # Stop searching through the regions if one has been found
                except:
                    print(f"NOT FOUND {regions[i]}")
        else:
            try:
                print(f"{region, name, riotGamesApiKey}")
                print(
                    f"https://{region.casefold()}.api.riotgames.com/lol/summoner/v4/summoners/by-name/{name.casefold()}?api_key={riotGamesApiKey}")
                with urllib.request.urlopen(
                        f"https://{region.casefold()}.api.riotgames.com/lol/summoner/v4/summoners/by-name/{name.casefold()}?api_key={riotGamesApiKey}") as url:
                    data = json.loads(url.read().decode())
                    correctRegion = region.casefold()
            except:
                print(f"error")
        name = data["name"]
        accountId = data["accountId"]
        summonerLevel = data["summonerLevel"]
        profileIconId = data["profileIconId"]
        try:
            with urllib.request.urlopen(
                    f"https://{correctRegion.casefold()}.api.riotgames.com/lol/match/v4/matchlists/by-account/{accountId}?api_key={riotGamesApiKey}") as url:
                data2 = json.loads(url.read().decode())
        except:
            print("error2")
        lane = []
        for i in range(0, len(data2)):
            lane.append(data2["matches"][i]["lane"])
        role = []
        for i in range(0, len(data2)):
            role.append(data2["matches"][i]["role"])
        champion = []
        for i in range(0, len(data2)):
            champion.append(data2["matches"][i]["champion"])
        totalGames = data2["totalGames"]
        embed = discord.Embed(title="League of Legends Stats", description="")
        embed.add_field(name="Name", value=f"{name}")
        embed.add_field(name="Region", value=f"{correctRegion}")
        # embed.add_field(name="Account ID", value=f"{accountId}")
        embed.add_field(name="Summoner Level", value=f"{summonerLevel}")
        embed.add_field(name="Favourite Lane", value=f"{most_frequent(lane)}")
        embed.add_field(name="Favourite Role", value=f"{most_frequent(role)}")
        embed.add_field(name="Favourite Champion", value=f"{most_frequent(champion)}")
        embed.add_field(name="Total Games", value=f"{totalGames}")
        embed.colour = (0xc28f2c)
        embed.set_footer(text="League of Legends",
                         icon_url="https://pbs.twimg.com/profile_images/1229450306343145472/eOInxRFz_400x400.png")
        end = time.time()
        embed.add_field(name="Time Taken", value=f"{round(end - start)} second(s)")
        await ctx.send(content=None, embed=embed)

    @commands.command(brief="UNRELEASED - Valorant Stats", description="Valorant Stats")
    async def valorant(self, ctx, name="DEFAULT", region="DEFAULT"):
        await ctx.send(f"GAME NOT RELEASED YET")

def setup(bot):
    bot.add_cog(Integrations(bot))
