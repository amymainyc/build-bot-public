import discord
from discord.ext import commands
import aiohttp
from mcuuid.api import GetPlayerData
from loguru import logger
import json

with open('data/database.json') as d:
    database = json.load(d)

class General(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        short_link = database["short_link"]
        activity = discord.Game(name=f"b.help | {short_link}")
        await self.client.change_presence(status=discord.Status.online, activity=activity)
        logger.info('Bot is ready.')


    @commands.command(aliases=['h'])
    async def help(self, ctx):
        embed = discord.Embed(title="How To Use Build Bot", color=0xFFA6FA)
        name = "About This Bot:"
        value = "Build Bot is the all-in-one bot for the Hypixel Guess The Build minigame. " \
                "Simply enter the given letters and Build Bot will return a list of possible answers. Have fun!"
        embed.add_field(name=name, value=value, inline=False)

        name = "Command: `b.answer (given letters)`"
        value = "Enter the given and missing letters after the command. " \
                "Replace underscores/missing letters with dashes (-). Do not use dashes for spaces. " \
                "Aliases: `b.ans`, `b.a`"
        embed.add_field(name=name, value=value, inline=False)

        name = "Example Usages:"
        value = "b.answer ch-ese-urg-r" \
                "\nb.ans ch-ese-urg-r" \
                "\nb.a ch-ese-urg-r"
        embed.add_field(name=name, value=value, inline=True)

        name = "Other Commands:"
        value = "`b.help`\n`b.invite`\n`b.stats`"
        embed.add_field(name=name, value=value, inline=True)

        short_link = database["short_link"]
        embed.set_footer(text=f"Invite and vote for build bot here > {short_link}")
        embed.set_thumbnail(url="https://i.imgur.com/Xjp1fJb.png")

        await ctx.send(embed=embed)


    @commands.command(aliases=['i'])
    async def invite(self, ctx):
        link = database["short_link"]
        message = "Invite Build Bot to your server using this link!" \
                  f"\n{link}"
        await ctx.send(message)


    @commands.command(aliases=['s'])
    async def stats(self, ctx, *username):
        if ctx.author == self.client.user:
            return
        if ctx.author.bot:
            return
        if len(username) != 1:
            await ctx.send("Please use the proper command format: `b.stats (username)`")
            return
        username = username[0]
        if self.checkusername(username) == -1:
            await ctx.send(
                "Invalid username. Please check your spelling and if you used the command correctly. "
                "\nProper usage: `b.stats (username)`"
            )
            return
        else:
            playername = self.checkusername(username)[1]
            playeruuid = self.checkusername(username)[0]

        await ctx.send('Showing Build Battle stats for ' + playername + '...')
        link = database["stat_site"]
        link = link.replace("[uuid]", playeruuid)
        link = link.replace("[key]", database["api_key"])
        logger.info(f'Finding Build Battle stats for {playername}: {link}')
        async with aiohttp.ClientSession() as session:
            async with session.get(link) as data:
                data = await data.json()

        if data["success"] is False:
            cause = data["cause"]
            logger.info(f"Error occurred whilst contacting Hypixel API: {cause}")
            await ctx.send("Error occurred whilst contacting Hypixel API. Please try again later.")
            return

        # general stats
        bbstats = data["player"]["stats"]["BuildBattle"]

        if "score" not in bbstats:
            rawscore = 0
            score = '0'
        else:
            rawscore = bbstats["score"]
            score = self.numberformatter(bbstats["score"])
        if "coins" not in bbstats:
            coins = '0'
        else:
            coins = self.numberformatter(bbstats["coins"])
        if "games_played" not in bbstats:
            games_played = '0'
        else:
            games_played = self.numberformatter(bbstats["games_played"])
        if "wins" not in bbstats:
            wins = '0'
        else:
            wins = self.numberformatter(bbstats["wins"])
        try:
            win_percent = str(round(bbstats["wins"] / bbstats["games_played"] * 100))
        except:
            win_percent = '0'

        if "wins_solo_normal" not in bbstats:
            wins_solo_normal = '0'
        else:
            wins_solo_normal = self.numberformatter(bbstats["wins_solo_normal"])
        if "solo_most_points" not in bbstats:
            solo_most_points = '0'
        else:
            solo_most_points = self.numberformatter(bbstats["solo_most_points"])

        if "wins_teams_normal" not in bbstats:
            wins_teams_normal = '0'
        else:
            wins_teams_normal = self.numberformatter(bbstats["wins_teams_normal"])
        if "teams_most_points" not in bbstats:
            teams_most_points = '0'
        else:
            teams_most_points = self.numberformatter(bbstats["teams_most_points"])

        if "wins_solo_pro" not in bbstats:
            wins_solo_pro = '0'
        else:
            wins_solo_pro = self.numberformatter(bbstats["wins_solo_pro"])

        if "wins_guess_the_build" not in bbstats:
            wins_guess_the_build = '0'
        else:
            wins_guess_the_build = self.numberformatter(bbstats["wins_guess_the_build"])
        if "correct_guesses" not in bbstats:
            correct_guesses = '0'
        else:
            correct_guesses = self.numberformatter(bbstats["correct_guesses"])

        # check what rank they are
        with open("data/ranks.json") as f:
            ranks = json.load(f)

        for rank in ranks:
            if ranks[rank] < rawscore:
                player_rank = rank

        embed = discord.Embed(title=f"{playername}'s Build Battle Stats", color=0xFFA6FA)
        embed.add_field(
            name=f"Rank: {player_rank} \n",
            value=f"Score: {score} \n"
                  f"Coins: {coins} \n"
                  f"Games Played: {games_played} \n"
                  f"Games Won: {wins} \n"
                  f"Win Percentage: {win_percent}% \n\n",
            inline=False
        )
        embed.add_field(
            name=f"**Solo Mode** \n",
            value=f"Games Won: {wins_solo_normal} \n"
                  f"Most Points: {solo_most_points} \n\n",
            inline=False
        )
        embed.add_field(
            name=f"**Teams Mode** \n",
            value=f"Games Won: {wins_teams_normal} \n"
                  f"Most Points: {teams_most_points} \n\n",
            inline=False
        )
        embed.add_field(
            name=f"**Pro Mode** \n",
            value=f"Games Won: {wins_solo_pro} \n\n",
            inline=False
        )
        embed.add_field(
            name=f"**Guess The Build** \n",
            value=f"Games Won: {wins_guess_the_build} \n"
                  f"Correct Guesses: {correct_guesses}",
            inline=False
        )
        embed.set_thumbnail(url=f"https://crafatar.com/avatars/{playeruuid}?size=40&default=MHF_Steve&overlay.png")
        link = database["short_link"]
        embed.set_footer(text=f"b.help | {link}")
        await ctx.send(embed=embed)


    def checkusername(self, arg):
        player = GetPlayerData(arg)
        if player.valid is True:
            return [player.uuid, player.username]
        else:
            return -1


    def numberformatter(self, price):
        price = str(price)
        if len(price) > 9:
            price = price[:-3] + ',' + price[-3:]
            price = price[:-7] + ',' + price[-7:]
            price = price[:-10] + ',' + price[-10:]
        elif len(price) > 6:
            price = price[:-3] + ',' + price[-3:]
            price = price[:-7] + ',' + price[-7:]
        elif len(price) > 3:
            price = price[:-3] + ',' + price[-3:]
        else:
            pass
        return price


def setup(client):
    client.add_cog(General(client))
