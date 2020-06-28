import googlemaps
import discord
from discord.ext import commands
import arrow as ar
import settings
import asyncio
from pathlib import Path

data_folder = Path("files/")

from master import get_prefix
bot = commands.Bot(command_prefix=get_prefix)
gmaps = googlemaps.Client(key=settings.GMAPS)
token = settings.TOKEN
from master import get_color
userSend = discord.Member

month = ["months", "month", "mo", "mos"]
week = ["weeks", "week", "wk", "wks"]
day = ["days", "day", "dy", "dys"]
hour = ["hours", "hour", "hr", "hrs"]
min = ["minutes", "minute", "min", "mins"]
csv_columns = ["timeAdd", "user", "timeCreated", "message"]
loopDict = {}
addDict = {}

resetLoop = False

# Sends a DM to a user
async def sendDM(input):
    timeAdd = input["timeAdd"]
    user = input["user"]
    timeCreated = input["timeCreated"]
    message = input["message"]
    channel = await userSend.create_dm()
    color = int(get_color(bot, channel.message))
    embed = discord.Embed(title="⏲ Your reminder is here! ⏲", colour=discord.Colour(color))
    embed.add_field(name = "The reminder was set at:", value = timeCreated + " UTC" )
    embed.add_field(name = "Your message is:", value = message)
    await channel.send(embed = embed)

# Either creates or adds to a loop
async def addToLoop(self, input: dict):
    global loopDict
    global resetLoop
    length = len(loopDict)
    if length == 0:
        task = asyncio.create_task(runLoop())
        resetLoop = False
        loopDict[str(length)] = (input)
    else: 
        resetLoop = True
        loopDict[str(length)] = (input)
        resetLoop = False
    
# Main looping function—never ends! 
async def runLoop():
    global resetLoop
    global loopDict
    global addDict
    while True:
        if resetLoop == False:
            for key in list(loopDict):
                if loopDict[key]["timeAdd"] == 0:
                    await sendDM(loopDict[key])
                    del loopDict[key]
                loopDict[key]["timeAdd"] -= 1
        elif resetLoop == True:
            break
        await asyncio.sleep(60)

# Formats various lengths to minutes
def formatToMin(self, inFormat, difference):
        if inFormat in min:
            return difference
        elif inFormat in hour:
            return difference * 60
        elif inFormat in day:
            return difference * 1440
        elif inFormat in week:
            return difference * 10080
        elif inFormat in month:
            return difference * 43800
    

class ReminderListener(commands.Cog):
    @bot.command()
    async def remind(self, ctx, *arg,):
        global userSend
        command = []
        if type(arg[0]) == discord.Member:
            userSend = discord.Member
        else:
            userSend = ctx.message.author 
        message = arg[1]
        arg = list(arg)
        del(arg[:1])
        for args in arg: 
            command.append(args)
        args = 0
        length = len(command)
        i = 0
        arguments = []
        timeAdd = 0
        timeNow = ar.utcnow()
        timeCreated = timeNow.format("MMMM Do, YYYY [at] DD:mm")
        while i < (length - 1):
            additional = formatToMin(self, command[i+1], int(command[i]))
            timeAdd += additional
            i += 2
        dictToSend = dict({"timeAdd": timeAdd, "user": userSend.id, "timeCreated": timeCreated, "message": message})
        await addToLoop(self, dictToSend)
        color = int(get_color(bot, ctx.message))
        embed = discord.Embed(title="⏲ Your reminder is set! ⏲", colour=discord.Colour(color))
        embed.add_field(name = "You will be reminded in:", value = str(timeAdd) + " minutes")
        embed.add_field(name = "Your message is:", value = message)
        await ctx.send(embed = embed)

    @remind.error
    async def remind_error(self, ctx, error):
        prefix = get_prefix(bot, ctx.message)
        color = int(get_color(bot, ctx.message))
        embed = discord.Embed(title="Syntax error >:(", colour = discord.Colour(color))
        embed.add_field(name = "Correct syntax:", value = "{}?remind @user \"message\" time`\ne.g. `?remind @TimeVibe \"Your message here\" 1 week 10 hours 3 minutes` \n \n *`@user` field is optional if the reminder is for yourself.*".format(prefix))
        message = await ctx.send(embed = embed)
        await asyncio.sleep(5)
        await message.delete()

        
def setup(client):
    client.add_cog(ReminderListener(client))
    print('ReminderListener is Loaded') 