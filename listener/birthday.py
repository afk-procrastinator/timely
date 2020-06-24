import discord
from discord.ext import commands
import arrow
import settings
import json
import arrow
from master import get_prefix
from master import get_color

bot = commands.Bot(command_prefix=get_prefix)
token = settings.TOKEN

def writeFile(combined, ctx, user):
    with open('files/{}.json'.format(ctx.guild.id), 'r+') as file:
        addData = {"usersbday":{str(user.id): combined}}
        data = json.load(file)
        data.update(addData)
        file.seek(0)
        file.truncate()
        json.dump(data, file, indent=4)

class BirthdayListener(commands.Cog):
    @bot.command()
    async def bdayset(self, ctx, *args):
        user = ctx.message.author
        prefix = get_prefix(bot, ctx.message)
        combined = " ".join(args) # i.e. 3 Jan
        try:
            date = arrow.get(combined, "MMMM D")
            writeFile(combined, ctx, user)
            color = int(get_color(bot, ctx.message))
            embed = discord.Embed(title="Birthday set!", colour=discord.Colour(color))
            embed.add_field(name="🎂🎂🎂", value="Set to: {0}".format(date))
            await user.send(embed = embed)
        except ValueError:
            embed = discord.Embed(title="Birthday error!", colour=discord.Colour(color))
            embed.add_field(name=">:(", value="Please try again, or type `{}help`".format(prefix))
            await user.send(embed = embed)
            
    @bot.command()
    async def bday(self, ctx, user: discord.Member):
        userID = user.id
        userNick = user.nick
        color = int(get_color(bot, ctx.message))
        with open('files/{}.json'.format(ctx.guild.id), 'r') as file:
            try:
                data = json.load(file)
                birthday = data["usersbday"][str(userID)]
                date = birthday.capitalize()
                embed = discord.Embed(title="{0}'s Birthday:".format(userNick), colour=discord.Colour(color))
                embed.add_field(name="🎂🎂🎂", value="Their birthday is: **{0}**".format(date))
                await ctx.send(embed = embed)
            except KeyError:
                prefix = get_prefix(bot, ctx.message)
                embed = discord.Embed(title="No Birthday Set!", colour=discord.Colour(color))
                embed.add_field(name="🎂🎂🎂", value="{0} doesn't have a birthday set! Use `{1}bdayset MONTH DAY` to set it.".format(userNick, prefix))
                await ctx.send(embed = embed)
                
    @bdayset.error
    async def bdayset_error(self, ctx, error):
        prefix = get_prefix(bot, ctx.message)
        color = int(get_color(bot, ctx.message))
        embed = discord.Embed(title="Error!", colour=discord.Colour(color))
        embed.add_field(name=">:(", value="Please try again, or type `{}help`".format(prefix))
        await ctx.send(embed = embed)    

    @bday.error
    async def bday_error(self, ctx, error):
        prefix = get_prefix(bot, ctx.message)
        color = int(get_color(bot, ctx.message))
        embed = discord.Embed(title="Error!", colour=discord.Colour(color))
        embed.add_field(name=">:(", value="Please try again, or type `{}help`".format(prefix))
        await ctx.send(embed = embed)    
    

def setup(client):
    client.add_cog(BirthdayListener(client))
    print('BirthdayListener is Loaded') 