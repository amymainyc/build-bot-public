import discord
from discord.ext import commands
from loguru import logger
import json
import math

with open('data/database.json') as d:
    database = json.load(d)

class Answer(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['ans', 'a'])
    async def answer(self, ctx, *param):
        errormessage = "Please specify the given letters and missing letters as dashes.\n"\
            "Correct usage example: `b.answer ch-ese-urg-r`"
        if ctx.author == self.client.user:
            return
        if param == ():
            await ctx.send(errormessage)
            return
        originalparam = ' '.join(param).lower()
        param = ''.join(param).lower()
        for char in param:
            if ord(char) != 45 and not 97 <= ord(char) <= 122:
                await ctx.send(errormessage)
                return

        # checks passed

        # get possible answers
        with open("data/themes.txt", "r") as f:
            possible = f.read()
            possible = possible.split('\n')

        # compare answers
        possiblethemes = []
        for ans in possible:
            original = ans
            ans = ans.split(' ')
            ans = ''.join(ans).lower()

            if len(ans) != len(param):
                match = False
            else:
                match = True
                for char in range(len(param)):
                    if ord(param[char]) != 45:
                        if param[char] == ans[char]:
                            pass
                        else:
                            match = False
                            break
            if match is True:
                possiblethemes.append(original)

        # send possible themes
        if possiblethemes == []:
            await ctx.send(f"No themes matching `{originalparam}`.")
            return

        pages = []
        totalthemes = len(possiblethemes)
        totalpages = math.floor(totalthemes / 20) + 1

        # page 1
        if totalpages == 1:
            pages.insert(0, self.makeembed(possiblethemes, '1', totalpages, totalthemes))
        elif 1 < totalpages:
            pages.insert(0, self.makeembed(possiblethemes[0:20], '1', totalpages, totalthemes))

        # page 2
        if totalpages == 2:
            pages.insert(1, self.makeembed(possiblethemes[20:], '2', totalpages, totalthemes))
        elif 2 < totalpages:
            pages.insert(1, self.makeembed(possiblethemes[20:40], '2', totalpages, totalthemes))

        # page 3
        if totalpages == 3:
            pages.insert(2, self.makeembed(possiblethemes[40:], '3', totalpages, totalthemes))
        elif 3 < totalpages:
            pages.insert(2, self.makeembed(possiblethemes[40:60], '3', totalpages, totalthemes))

        # page 4
        if totalpages == 4:
            pages.insert(3, self.makeembed(possiblethemes[60:], '4', totalpages, totalthemes))
        elif 4 < totalpages:
            pages.insert(3, self.makeembed(possiblethemes[60:80], '4', totalpages, totalthemes))

        # page 5
        if totalpages == 5:
            pages.insert(4, self.makeembed(possiblethemes[80:], '5', totalpages, totalthemes))
        elif 5 < totalpages:
            pages.insert(4, self.makeembed(possiblethemes[80:100], '5', totalpages, totalthemes))

        # page 6
        if totalpages == 6:
            pages.insert(5, self.makeembed(possiblethemes[100:], '6', totalpages, totalthemes))
        elif 6 < totalpages:
            pages.insert(5, self.makeembed(possiblethemes[100:120], '6', totalpages, totalthemes))

        # page 7
        if totalpages == 7:
            pages.insert(6, self.makeembed(possiblethemes[120:], '7', totalpages, totalthemes))
        elif 7 < totalpages:
            pages.insert(6, self.makeembed(possiblethemes[120:140], '7', totalpages, totalthemes))

        # page 8
        if totalpages == 8:
            pages.insert(7, self.makeembed(possiblethemes[140:], '8', totalpages, totalthemes))
        elif 8 < totalpages:
            pages.insert(7, self.makeembed(possiblethemes[140:160], '8', totalpages, totalthemes))

        # page 9
        if totalpages == 9:
            pages.insert(8, self.makeembed(possiblethemes[160:], '9', totalpages, totalthemes))
        elif 9 < totalpages:
            pages.insert(8, self.makeembed(possiblethemes[160:180], '9', totalpages, totalthemes))

        # page 10
        if totalpages == 10:
            pages.insert(9, self.makeembed(possiblethemes[180:], '10', totalpages, totalthemes))
        elif 10 < totalpages:
            pages.insert(9, self.makeembed(possiblethemes[180:200], '10', totalpages, totalthemes))

        # page 11
        if totalpages == 11:
            pages.insert(10, self.makeembed(possiblethemes[200:], '11', totalpages, totalthemes))
        elif 11 < totalpages:
            pages.insert(10, self.makeembed(possiblethemes[200:220], '11', totalpages, totalthemes))

        # page 12
        if totalpages == 12:
            pages.insert(11, self.makeembed(possiblethemes[220:], '12', totalpages, totalthemes))
        elif 12 < totalpages:
            pages.insert(11, self.makeembed(possiblethemes[220:240], '12', totalpages, totalthemes))

        # page 13
        if totalpages == 13:
            pages.insert(12, self.makeembed(possiblethemes[240:], '13', totalpages, totalthemes))
        elif 13 < totalpages:
            pages.insert(12, self.makeembed(possiblethemes[240:260], '13', totalpages, totalthemes))

        # page 14
        if totalpages == 14:
            pages.insert(13, self.makeembed(possiblethemes[260:], '14', totalpages, totalthemes))
        elif 14 < totalpages:
            pages.insert(13, self.makeembed(possiblethemes[260:280], '14', totalpages, totalthemes))

        # page 15
        if totalpages == 15:
            pages.insert(14, self.makeembed(possiblethemes[280:], '15', totalpages, totalthemes))
        elif 15 < totalpages:
            pages.insert(14, self.makeembed(possiblethemes[280:380], '15', totalpages, totalthemes))

        # page 16
        if totalpages == 16:
            pages.insert(15, self.makeembed(possiblethemes[300:], '16', totalpages, totalthemes))
        elif 16 < totalpages:
            pages.insert(15, self.makeembed(possiblethemes[300:320], '16', totalpages, totalthemes))

        if totalpages == 1:
            await ctx.send(embed=pages[0])
            return

        left = '⏪'
        right = '⏩'

        index = 0
        msg = None
        action = ctx.send
        while True:
            res = await action(embed=pages[index])
            if res is not None:
                msg = res
            l = index != 0
            r = index != len(pages) - 1
            await msg.add_reaction(left)
            await msg.add_reaction(right)
            react, user = await self.client.wait_for('reaction_add', check=self.predicate(msg, l, r))
            if react.emoji == left and l:
                index -= 1
            elif react.emoji == right and r:
                index += 1
            action = msg.edit


    def predicate(self, message, l, r):
        def check(reaction, user):
            left = '⏪'
            right = '⏩'
            if reaction.message.id != message.id or user == self.client.user:
                return False
            if l and reaction.emoji == left:
                return True
            if r and reaction.emoji == right:
                return True
            return False

        return check


    def makeembed(self, possiblethemes, page, totalpages, totalthemes):
        length = math.ceil(len(possiblethemes) / 2)
        possiblethemes1 = '\n'.join(possiblethemes[:length])
        possiblethemes2 = '\n'.join(possiblethemes[length:])
        if totalthemes == 1:
            embed = discord.Embed(title=f"{totalthemes} Possible Theme", color=0xFFA6FA)
        else:
            embed = discord.Embed(title=f"{totalthemes} Possible Themes", color=0xFFA6FA)
        embed.add_field(name=f"Showing Page {page} of {totalpages}", value=possiblethemes1)
        if possiblethemes2 != '':
            embed.add_field(name=f"** **", value=possiblethemes2)
        embed.set_footer(text=f"Theme not here? Feel free to dm me! Moonflower#8861")
        return embed


def setup(client):
    client.add_cog(Answer(client))
