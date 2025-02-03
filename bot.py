import discord
import pytz
from datetime import datetime
from discord.ext import commands
from dotenv import load_dotenv
import os

load_dotenv()

# 建立 Bot 實例，使用 commands.Bot 而不是 discord.Bot
bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())

# 台北時區
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

    # 發送訊息給授權用戶
    AUTHORIZED_USER_ID = int(os.getenv("AUTHORIZED_USER_ID"))
    if AUTHORIZED_USER_ID:
        user = await bot.fetch_user(AUTHORIZED_USER_ID)
        await user.send(f"Hi! 機器人已上線")

# 載入 Cogs
initial_extensions = ["cogs.ping", "cogs.weather"]

if __name__ == "__main__":
    for extension in initial_extensions:
        bot.load_extension(extension)

# 啟動機器人
TOKEN = os.getenv("TOKEN")
bot.run(TOKEN)
