import discord
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("dc_bot_token")
bot = discord.Bot(intents = discord.Intents.all())

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}, datetime: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("Connected to the following servers:")
    for guild in bot.guilds:
        print(f"- {guild.name} (ID: {guild.id}), Members: {guild.member_count}")
    

bot.run(TOKEN)