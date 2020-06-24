import os
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

TOKEN = os.environ.get("DISCORD_TOKEN")
GMAPS = os.environ.get("GMAPS")
OMDB = os.environ.get("OMDB")