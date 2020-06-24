import discord
from discord.ext import commands
from discord.utils import get
from dotenv import load_dotenv
import asyncio
import json

botColor = 0xFFFFFF

def get_prefix(client, message):
    with open('files/{}.json'.format(message.guild.id), 'r+') as f:
        prefixes = json.load(f)
    return prefixes["info"]["prefix"]

def get_color(client, message):
    with open('files/{}.json'.format(message.guild.id), 'r+') as f:
        colors = json.load(f) 
    hex_str = colors["info"]["color"]
    hex_int = int(hex_str, 16)
    new_int = hex_int + 0x200
    if new_int > 16777215:
        new_int = 16777214
    return new_int