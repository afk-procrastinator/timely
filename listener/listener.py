import googlemaps
from timezonefinder import TimezoneFinder
import discord
from discord.ext import commands
import settings

from master import get_prefix
bot = commands.Bot(command_prefix=get_prefix)
gmaps = googlemaps.Client(key=settings.GMAPS)
token = settings.TOKEN
tf = TimezoneFinder()
lat = 0
from master import get_color
lon = 0
region = ""
timeVibeRole = False
cancelTimer = False

threads = []

month = ["months", "month", "mo", "mos"]
week = ["weeks", "week", "wk", "wks"]
day = ["days", "day", "dy", "dys"]
hour = ["hours", "hour", "hr", "hrs"]
min = ["minutes", "minute", "min", "mins"]

csv_columns = ["timeAdd", "user", "timeCreated", "message", "guild"]
loopDict = {}
sendDict = {}

class GeneralListener(commands.Cog):
    
    # only allows Admin to call the setup()
    @bot.command()
    async def dddddsetup(self, ctx, input: str, *args: str):
        if input == "role":
            guild = ctx.guild
            selfRole = guild.roles
            for role in selfRole:
                if role == "TimeVibeRole":
                    timeVibeRole = True
                    await ctx.send("Bot role already exists!")
        if timeVibeRole == False:
            role = guild.create_role(name="TimeVibeRole")
            await role
            await bot.add_roles(bot, role)       
    # setup command error handling
    @dddddsetup.error
    async def dddddsetup_error(self, ctx, error):
       if isinstance(error, commands.MissingRequiredArgument):
        color = int(get_color(bot, ctx.message))
        embed = discord.Embed(title="**Argument error**", colour=discord.Colour(color))
        embed.add_field(name="Possible arguments:", value="`role` - creates role for bot, only needed for initialization.")
        await ctx.send(embed=embed)
    
def setup(client):
    client.add_cog(GeneralListener(client))
    print('GeneralListener is Loaded')   