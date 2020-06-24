import googlemaps
from timezonefinder import TimezoneFinder
import discord
from discord.ext import commands
import settings
import time
import asyncio
from master import get_color

from master import get_prefix
bot = commands.Bot(command_prefix=get_prefix)
gmaps = googlemaps.Client(key=settings.GMAPS)
token = settings.TOKEN
tf = TimezoneFinder()
lat = 0
lon = 0
region = ""
timeVibeRole = False
cancelTimer = False


month = ["months", "month", "mo", "mos"]
week = ["weeks", "week", "wk", "wks"]
day = ["days", "day", "dy", "dys"]
hour = ["hours", "hour", "hr", "hrs"]
min = ["minutes", "minute", "min", "mins"]

class TimerListener(commands.Cog):
    
    @bot.command()
    async def timer(self, ctx, arg1: int, arg2: str):
        units = ""
        color = int(get_color(bot, ctx.message))
        possibleCommands = ["seconds", "sec", "secs", "s", "minutes", "hours", "minute", "hour", "m", "mins", "hr", "hrs"]
        if arg2 in possibleCommands:
            units = arg2
        else:
            embed = discord.Embed(title="Timer error:", colour=discord.Colour(color))
            embed.add_field(name="Syntax error", value="Whoops! Syntax error. Command should be: \n ```?timer length unit``` \n Units can only be `hours`, `minutes`, or `seconds`. Please use the `?reminder` command for anything longer.")
            await ctx.send(embed = embed)
            return
        if arg2 in ["minutes", "minute", "m", "mins"]:
            arg1 = arg1 * 60
        elif arg2 in ["hours", "hour", "hr", "hrs"]:
            arg1 = arg1 * 3600
        totalTime = time.strftime("%H:%M:%S", time.gmtime(arg1))
        if arg1 > 43200:
            embed = discord.Embed(title="Timer too long!", colour=discord.Colour(color))
            embed.add_field(name="Progress Bar", value="Your timer is over 12 hours! Why don't you try the `?reminder` command instead?")
            await ctx.send(embed=embed)
            return
        t = 0
        while t < arg1 + 1:
            bar_length = 20
            percent = float(t) / arg1
            arrow = '-' * int(round(percent * bar_length)-1) + '>'
            spaces = ' ' * (bar_length - len(arrow))
            timeRemaining = time.strftime("%H:%M:%S", time.gmtime(int(arg1-t)))
            string = ("```\rPercent: [{0}] {1}%```".format(arrow + spaces, int(round(percent * 100))))
            embed = discord.Embed(title="⏱: {0}".format(timeRemaining), colour=discord.Colour(color))
            embed.add_field(name="⏳", value=string)
            if t == 0:
                message = await ctx.send(embed=embed)
            else:
                await message.edit(embed=embed)
            t += 1
            await asyncio.sleep(1)
            if cancelTimer == True:
                string = ("_**CANCELLED_**")
                embed = discord.Embed(title="⏱", colour=discord.Colour(color))
                embed.add_field(name="⏱", value=string)
                return
        string = ("_**FINISHED**_")
        embed = discord.Embed(title="💫🎉🎉🎉💫", colour=discord.Colour(color))
        embed.add_field(name="💫🎉🎉🎉💫", value=string)
        await message.edit(embed=embed)

    @bot.command()
    async def cancel(self, ctx):
        global cancelTimer
        cancelTimer == True
    # error with the timer command 
    @timer.error
    async def timer_error(self, ctx, error):
        color = int(get_color(bot, ctx.message))
        embed = discord.Embed(title="**Syntax Error**", colour = discord.Color(color))
        prefix = get_prefix(bot, ctx.message)
        embed.add_field(name = "_**Please try again!**_", value = "Example: \n`{}timer 10 seconds`".format(prefix))
        message = await ctx.send(embed = embed)
        await asyncio.sleep(2)
        await message.delete()

    @cancel.error
    async def cancel_error(self, ctx, error):
        prefix = get_prefix(bot, ctx.message)
        color = int(get_color(bot, ctx.message))
        embed = discord.Embed(title="Error!", colour=discord.Colour(color))
        embed.add_field(name=">:(", value="Please try again, or type `{}help`".format(prefix))
        await ctx.send(embed = embed)   
    

def setup(client):
    client.add_cog(TimerListener(client))
    print('TimerListener is Loaded')   