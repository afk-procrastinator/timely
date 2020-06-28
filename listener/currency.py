import discord
from discord.ext import commands
import settings
import asyncio
import json
import requests
from master import get_color
from master import get_prefix
bot = commands.Bot(command_prefix=get_prefix)

token = settings.TOKEN

currenciesFirst = '''
`CAD` : Canadian Dollar
`HKD` : Hong Kong Dollar
`ISK` : Iceland Krona	
`PHP` : Philippine Peso	
`DKK` : Danish Krone	
`HUF` : Forint [Hungary]
`CZK` : Czech Koruna	
`GBP` : British Pound 
`RON` : New Romanian Lee
`SEK` : Swedish Krona	
`IDR` : Rupiah [Indonesia]
`INR` : Indian Rupee
`BRL` : Brazilian Real	
`RUB` : Russian Ruble
`HRK` : Croatian Kuna	
`JPY` : Japanese Yen
'''

currenciesSecond = '''
`THB` : Bhat [Thailand]
`CHF` : Swiss Franc
`EUR` : Euro
`MYR` : Malaysian Ringgit	
`BGN` : Bulgarian Lev	
`TRY` : Turkish Lira	
`CNY` : Yuan Renminbi [China]
`NOK` : Norwegian Krone	
`NZD` : New Zealand Dollar
`ZAR` : Rand [Lesotho]
`USD` : United States Dollar
`SGD` : Singapore Dollar	
`AUD` : Australian Dollar
`ILS` : New Israeli Sheqel	
`KRW` : Won [Korea]
`PLN` : Zloty [Poland]
'''

async def getAPI(self, base, currency):
    response = requests.get("https://api.exchangeratesapi.io/latest?base={}".format(base))
    data = json.loads(response.text)
    return data["rates"][currency]

class CurrencyListener(commands.Cog):
    @bot.command()
    async def convert(self, ctx, amount, base: str, to: str, currency: str):
        color = int(get_color(bot, ctx.message))
        base = base.upper()
        currency = currency.upper()
        response = await getAPI(self, base, currency)
        amount = int(amount)
        final = round((amount * response), 2)
        embed = discord.Embed(title="💸💸💸", colour=discord.Colour(color))
        embed.add_field(name = "Converting {0} to {1}".format(base, currency), value = "`{0}` `{1}` in `{2}` is \n `{3} {4}`".format(amount, base, currency, final, currency), inline=True)
        embed.set_footer(text = "Thanks to exchangeratesapi.io for the data!")
        await ctx.send(embed = embed)

    @convert.error
    async def convertError(self, ctx, error):
        prefix = get_prefix(bot, ctx.message)
        color = int(get_color(bot, ctx.message))
        embed = discord.Embed(title="Possible currencies:", colour=discord.Colour(color))
        embed.add_field(name="Syntax", value="`{}convert 10 USD RUB`".format(prefix), inline = False)
        embed.add_field(name = "💸💸💸💸💸💸", value = currenciesFirst, inline=True)
        embed.add_field(name = "💸💸💸💸💸💸", value = currenciesSecond, inline=True)
        embed.set_footer(text = "Thanks to exchangeratesapi.io for the data!")
        message = await ctx.send(embed = embed)
        await asyncio.sleep(5)
        await message.delete()
        

    
def setup(client):
    client.add_cog(CurrencyListener(client))
    print('CurrencyListener is Loaded') 