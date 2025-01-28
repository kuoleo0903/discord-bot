import discord
from discord.errors import NotFound
import requests
from datetime import datetime
from os import getenv
import json
from dotenv import load_dotenv
import pytz

load_dotenv()

bot = discord.Bot(intents=discord.Intents.all())

# 假設您要將時間轉換為台北時間
taipei_tz = pytz.timezone('Asia/Taipei')
    
# 取得當前 UTC 時間並轉換為台北時間
utc_now = datetime.now(pytz.utc)
taipei_now = utc_now.astimezone(taipei_tz)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}, datetime: {taipei_now.strftime('%Y-%m-%d %H:%M:%S')}")
    print("Connected to the following servers:")
    for guild in bot.guilds:
        print(f"- {guild.name} (ID: {guild.id}), Members: {guild.member_count}")
    user = await bot.fetch_user(AUTHORIZED_USER_ID)
    await user.send(f"Hi! {taipei_now.strftime('%Y-%m-%d %H:%M:%S')}")
    
AUTHORIZED_USER_ID = 439814891176460299  # 替換成你的 Discord 使用者 ID


bot.run(getenv("TOKEN"))