import discord
import pytz
from datetime import datetime
from discord.ext import commands
from dotenv import load_dotenv
import os

load_dotenv()

bot = commands.Bot(intents=discord.Intents.all())

# 台北時區
taipei_tz = pytz.timezone('Asia/Taipei')


@bot.event
async def on_ready():
    # 取得當前 UTC 時間並轉換為台北時間
    utc_now = datetime.now(pytz.utc)
    taipei_now = utc_now.astimezone(taipei_tz)
    print(f"Logged in as {bot.user}, datetime: {taipei_now.strftime('%Y-%m-%d %H:%M:%S')}")
    print("Connected to the following servers:")
    for guild in bot.guilds:
        print(f"- {guild.name} (ID: {guild.id}), Members: {guild.member_count}")

    # 只發送訊息給開發者
    AUTHORIZED_USER_ID = int(os.getenv("AUTHORIZED_USER_ID"))
    if AUTHORIZED_USER_ID:
        user = await bot.fetch_user(AUTHORIZED_USER_ID)
        await user.send(f"Hi! 機器人已上線")

if __name__ == "__main__":
    cogs_path = './cogs'
    if os.path.exists(cogs_path):
        for foldername in os.listdir(cogs_path):
            # 確保是一個資料夾，且裡面有 cog.py
            subdir = os.path.join(cogs_path, foldername)
            if os.path.isdir(subdir) and 'cog.py' in os.listdir(subdir):
                # 轉換成路徑格式: cogs.folder_name.cog
                extension = f'cogs.{foldername}.cog'
                try:
                    bot.load_extension(extension)
                    print(f"✅ 成功載入: {extension}")
                except Exception as e:
                    print(f"❌ 載入失敗 {extension}: {e}")
    else:
        print("⚠ 找不到 cogs 資料夾")

TOKEN = os.getenv("TOKEN")
bot.run(TOKEN)
