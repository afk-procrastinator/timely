import discord
from discord.ext import commands
import settings
import asyncio
import requests
import re
import json
from pathlib import Path
from master import get_prefix
from master import get_color

data_folder = Path("files/")

token = settings.TOKEN
bot = commands.Bot(command_prefix=get_prefix)
bot.remove_command("help")


mainString = """
`tz`
`convert`
`distance`
`reminder/timer`
`birthday`
`fun`
`utility`
`support`

*Type `{0}help CATEGORY` to see command syntax*
*Type `{0}help data` to see where and how we use your data.*
"""
supportString = """
I am but a solo developer working on this bot using the discord.py async rewrite, so bugs and issues will be common.
`{0}contact MESSAGE` will send me a message- if you notice any bugs, please send them there. Spam and certain keywords will be blocked. 
All of the code is open-source on my [GitHub](https://github.com/spenmich1/timevibeBot).
Donate to me via PayPal [spencermichaels1@gmail.com] or BTC: [1Mf3oAadsGJVN39Up9gZwQdQneMy6DDc2c].

Or, spread my links:
[bots.gg](https://discord.bots.gg/bots/717002097790550038)
[bots on discord](https://bots.ondiscord.xyz/bots/717002097790550038)
[abstract discord list](https://abstractlist.com/bot/717002097790550038)
[discord bot list](https://discordbotlist.com/bots/timely)
[top.gg](https://top.gg/bot/717002097790550038)
"""
tzString = """
*Gives the current time for a certain location or user:*
`{0}tz LOCATION`
`{0}tz USER`

*Sets your timezone for others to access:*
`{0}tzset LOCATION`
"""
convertString = """
*Converts an amount from one currency to another:*
`{0}convert AMOUNT CURRENCY to CURRENCY`
Type `{0}convert` to see a full list of supported currencies. 
"""
distanceString = """
*Gives the amount of time until a given date:*
`{0}dis DATE UNIT`
Date should be in DD/MM/YYYY format. Supported units: days, weeks, months, years. 
"""
reminderString = """
*Sets a timer for a given amount of time. Best for less than an hour.*
`{0}timer AMOUNT UNIT`

*Sets a reminder for a given date:*
`{0}remind USER "MESSAGE" AMOUNT UNIT`
*Make sure the message is in quotations. This command is still in construction, and may be buggy.*
"""
birthdayString = """
*Gives a user's birthday:*
`{0}bday USER`

*Sets your birthday for others to access:*
`{0}bdayset MON DAY`
*The month should be shortened: e.g. `aug`, `jan`, `mar`.
"""
funString = """
*Checks IMDB data on a movie:*
`{0}movie MOVIE`

*Checks How Long to Beat data on a videogame:*
`{0}hltb GAME`

*Generates a QR code of a certain text or url:*
`{0}qr TEXT`

*Gives the most common phrases and members in a given channel:*
`{0}messages CHANNEL AMOUNT`
*Ommiting the `CHANNEL` will return data for the channel the command was sent in.*
*You can also change `AMOUNT` with a certain length of time in hours, days, or weeks*,
"""
utilityString = """
*Sets a new prefix:*
`{0}prefix PREFIX`

*Sets a new color:*
`{0}colorset HEX`
"""

class botCommandsListener(commands.Cog):
        
    @bot.command()
    async def help(self, ctx, *args):
        prefix = get_prefix(bot, ctx.message)
        color = int(get_color(bot, ctx.message))
        if len(args) == 0:
            embed = discord.Embed(title="Help is here!", colour=color)
            embed.add_field(name=" __**Command Categories:**__", value=mainString.format(prefix))
            await ctx.send(embed=embed)
        elif args[0] == "tz":
            embed = discord.Embed(title="Help is here!", colour=color)
            embed.add_field(name=" __**Timezone Commands:**__", value=tzString.format(prefix))
            await ctx.send(embed=embed)
        elif args[0] == "convert":
            embed = discord.Embed(title="Help is here!", colour=color)
            embed.add_field(name=" __**Convert Commanbds:**__", value=convertString.format(prefix))
            await ctx.send(embed=embed)
        elif args[0] == "distance":
            embed = discord.Embed(title="Help is here!", colour=color)
            embed.add_field(name=" __**Distance Commands:**__", value=distanceString.format(prefix))
            await ctx.send(embed=embed)
        elif args[0] == "reminder/timer":
            embed = discord.Embed(title="Help is here!", colour=color)
            embed.add_field(name=" __**Reminder/Timer Commands:**__", value=reminderString.format(prefix))
            await ctx.send(embed=embed)
        elif args[0] == "birthday":
            embed = discord.Embed(title="Help is here!", colour=color)
            embed.add_field(name=" __**Birthday Commands:**__", value=birthdayString.format(prefix))
            await ctx.send(embed=embed)
        elif args[0] == "fun":
            embed = discord.Embed(title="Help is here!", colour=color)
            embed.add_field(name=" __**Fun Commands:**__", value=funString.format(prefix))
            await ctx.send(embed=embed)
        elif args[0] == "utility":
            embed = discord.Embed(title="Help is here!", colour=color)
            embed.add_field(name=" __**Utility Commands:**__", value=utilityString.format(prefix))
            embed.set_footer(text="Only users with Admin permissions can run these commands. Sorry normies.")
            await ctx.send(embed=embed)
        elif args[0] == "data":
            embed = discord.Embed(title="Help is here!", colour=color)
            embed.add_field(name=" __**How we use your data:**__", value="""By inviting me to your server, you only allow me to access the permissions you agreed on when adding me. I only collect data which you give to me, which inclues your birthday and timezone. 
                            
                            The timezone data is saved as **general regions**, not the location you type in. 
                            
                            The birthday data saves only what you give it, and **doesn't support year of birth** for a reason.
                            
                            The messaging parsing command only temporarily reads the messages in the server, and deletes **any mention** of the messages from it's instant memory as soon as it finishes. 
                            
                            All data saved is deleted upon leaving a server. We use the same hosting servers as many other leading bots who collect far more detailed information on you. """)
            await ctx.send(embed=embed)
        elif args[0] == "support":
            embed = discord.Embed(title="Help is here!", colour=color)
            embed.add_field(name=" __**Support me:**__", value=supportString.format(prefix))
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(title="Help is here!", colour=color)
            embed.add_field(name=" __**Command Categories:**__", value=mainString.format(prefix))
            await ctx.send(embed=embed)        
        
    @bot.command()
    async def friendship(self, ctx):
        user = ctx.message.author
        color = int(get_color(bot, ctx.message))
        embed = discord.Embed(title="Wanna be friends?", colour=discord.Colour(color))
        embed.add_field(name="<3 <3 <3", value="Just slid into your DMs! Now you can access commands from the comfort of your messages.")
        await user.send(embed=embed)

    @bot.command()
    @commands.has_permissions(administrator=True)
    async def prefix(self, ctx, *args):
        color = int(get_color(bot, ctx.message))
        if args:
            with open('files/{}.json'.format(ctx.guild.id), 'r') as f:
                prefixes = json.load(f)    
            prefixes["info"]["prefix"] = args[0]
            with open('files/{}.json'.format(ctx.guild.id), 'w' ) as f:
                f.truncate()
                json.dump(prefixes, f, indent = 4)
            prefix = get_prefix(bot, ctx.message)
            username = "Timely [{}]".format(prefix)
            await ctx.guild.get_member(717002097790550038).edit(nick=username)
            embed = discord.Embed(title="Prefix has been changed!", colour=discord.Color(color))
            embed.add_field(name="Your prefix has been updated!".format(prefix), value="The prefix for Timely is now: `{}`".format(prefix))
            await ctx.send(embed=embed)
        else:
            prefix = get_prefix(bot, ctx.message)
            embed = discord.Embed(title="Prefix settings!", colour=discord.Color(color))
            embed.add_field(name="Your current prefix is **{}**".format(prefix), value="Set a new prefix with `{}prefix PREFIX`".format(prefix))
            await ctx.send(embed=embed)
    
    @bot.command()
    @commands.has_permissions(administrator=True)
    async def color(self, ctx):
       with open('files/{}.json'.format(ctx.guild.id), 'r') as f:
           color = json.load(f)   
       hexa = color["info"]["color"]
       prefix = get_prefix(bot, ctx.message)
       hex_str = hexa
       hex_int = int(hex_str, 16)
       new_int = hex_int + 0x200
       hexa = hexa.replace("0x", "")
       if new_int > 16777215:
           new_int = 16777214
       url = "http://www.thecolorapi.com/id?hex={}".format(hexa)
       response = requests.get(url)
       data = json.loads(response.text)
       image = (data["image"]["named"])
       embed = discord.Embed(title="Color settings!", colour=new_int)
       embed.add_field(name="Your current color:", value="**#{0}**\nSet a new color with `{1}colorset HEX`".format(hex_str.replace("0x",""), prefix))
       embed.set_thumbnail(url="http://www.singlecolorimage.com/get/{}/100x100".format(hexa))
       await ctx.send(embed=embed)
    
    @bot.command()
    @commands.has_permissions(administrator=True)
    async def colorset(self, ctx, hex):
        hex = hex.replace("#", "")
        match = re.search(r'^(?:[0-9a-fA-F]{3}){1,2}$', hex)
        if match:
            with open('files/{}.json'.format(ctx.guild.id), 'r') as f:
                color = json.load(f)    
            color["info"]["color"] = "0x"+hex
            with open('files/{}.json'.format(ctx.guild.id), 'w' ) as f:
                f.truncate()
                json.dump(color, f, indent = 4)
            colorPriv = int(get_color(bot, ctx.message))
            embed = discord.Embed(title="Color settings!", colour=discord.Color(colorPriv))
            embed.add_field(name="Your new color:", value="hex")
            embed.set_thumbnail(url="http://www.singlecolorimage.com/get/{}/100x100".format(hex))
            await ctx.send(embed=embed)
        else:
            color = int(get_color(bot, ctx.message))
            embed = discord.Embed(title="Error:", colour=discord.Colour(color))
            embed.add_field(name="Not a valid hex code!", value="Please try again!")
            message = await ctx.send(embed = embed)
            await asyncio.sleep(5)
            await message.delete()

    @colorset.error
    async def colorset_error(self, ctx, error):
        prefix = get_prefix(bot, ctx.message)
        color = int(get_color(bot, ctx.message))
        embed = discord.Embed(title="Error!", colour=discord.Colour(color))
        embed.add_field(name=">:(", value="Please try again, or type `{}help`".format(prefix))
        await ctx.send(embed = embed)    
        
    @color.error
    async def color_error(self, ctx, error):
        prefix = get_prefix(bot, ctx.message)
        color = int(get_color(bot, ctx.message))
        embed = discord.Embed(title="Error!", colour=discord.Colour(color))
        embed.add_field(name=">:(", value="Please try again, or type `{}help`".format(prefix))
        await ctx.send(embed = embed)    
        
    @friendship.error
    async def friendship_error(self, ctx, error):
        prefix = get_prefix(bot, ctx.message)
        color = int(get_color(bot, ctx.message))
        embed = discord.Embed(title="Error!", colour=discord.Colour(color))
        embed.add_field(name=">:(", value="Please try again, or type `{}help`".format(prefix))
        await ctx.send(embed = embed)    
    '''
    @prefix.error
    async def prefix_error(self, ctx, error):
        prefix = get_prefix(bot, ctx.message)
        color = int(get_color(bot, ctx.message))
        embed = discord.Embed(title="Error!", colour=discord.Colour(color))
        embed.add_field(name=">:(", value="Please try again, or type `{}help`".format(prefix))
        await ctx.send(embed = embed)   
        '''
    @friendship.error
    async def friendship_error(self, ctx, error):
        prefix = get_prefix(bot, ctx.message)
        color = int(get_color(bot, ctx.message))
        embed = discord.Embed(title="Error!", colour=discord.Colour(color))
        embed.add_field(name=">:(", value="Please try again, or type `{}help`".format(prefix))
        await ctx.send(embed = embed)   

    @help.error
    async def help_error(self, ctx, error):
        prefix = get_prefix(bot, ctx.message)
        color = int(get_color(bot, ctx.message))
        embed = discord.Embed(title="Error!", colour=discord.Colour(color))
        embed.add_field(name=">:(", value="Please try again, or type `{}help`".format(prefix))
        await ctx.send(embed = embed)   
        
        
def setup(client):
    client.add_cog(botCommandsListener(client))
    print('botCommandsListener is Loaded') 
