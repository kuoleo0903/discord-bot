import discord
from discord.errors import NotFound
import requests
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("dc_bot_token")  # 從環境變數取得 Bot Token
AUTHORIZED_USER_ID = 439814891176460299  # 替換成你的 Discord 使用者 ID

bot = discord.Bot()  # 使用 discord.Bot 來支援斜線指令

def get_public_ip():
    """從外部 API 獲取伺服器的對外 IP"""
    try:
        response = requests.get("https://api.ipify.org?format=text")
        if response.status_code == 200:
            return response.text
        else:
            return "無法取得 IP，請稍後再試"
    except Exception as e:
        return f"發生錯誤: {e}"

@bot.slash_command(name="get_server_ip", description="取得伺服器的對外 IP")
async def get_server_ip(ctx: discord.ApplicationContext):
    """處理 /get_server_ip 指令"""
    if ctx.author.id == AUTHORIZED_USER_ID:
        ip = get_public_ip()
        await ctx.author.send(f"伺服器的對外 IP 是：{ip}")
        try:
            await ctx.respond("已將伺服器 IP 發送至你的私訊！", ephemeral=True)
        except NotFound as e:
            await ctx.respond("交互過期或無效，請重新執行命令。")
    else:
        await ctx.respond("你無權使用此指令。", ephemeral=True)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}, datetime: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("Connected to the following servers:")
    for guild in bot.guilds:
        print(f"- {guild.name} (ID: {guild.id}), Members: {guild.member_count}")

bot.run(TOKEN)
