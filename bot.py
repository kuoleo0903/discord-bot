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

# 轉換為台北時區
taipei_tz = pytz.timezone('Asia/Taipei')
    
# 取得當前 UTC 時間並轉換為台北時區
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
    
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.content == "ping":
        await message.channel.send("pong")
        
    if message.content.startswith("hello"):
        await message.channel.send("Hello! How are you?")

AUTHORIZED_USER_ID = int(getenv("AUTHORIZED_USER_ID"))  # Discord 使用者 ID

# ----------------------------------------------------------------------------

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

@bot.slash_command(description="取得伺服器的對外 IP")
async def get_server_ip(ctx):
    """處理 /get_server_ip 指令"""
    if ctx.author.id == AUTHORIZED_USER_ID:
        ip = get_public_ip()
        try:
            if ctx.channel.type == discord.ChannelType.private:
                await ctx.respond(f"伺服器的對外 IP 是：{ip}")
            else:
                await ctx.author.send(f"伺服器的對外 IP 是：{ip}")
                await ctx.respond("已將伺服器 IP 發送至你的私訊！", ephemeral=True)
        except NotFound as e:
            await ctx.respond("交互過期或無效，請重新執行命令。")
    else:
        await ctx.respond("你無權使用此指令。", ephemeral=True)
        
# ----------------------------------------------------------------------------

@bot.slash_command(description="查看機器人是否上線")
async def check_online(ctx):
    """處理 /check_online 指令"""
    await ctx.respond("機器人正常運行中！")
    
@bot.slash_command(description="加法計算機")
async def add(ctx, num1: int, num2: int):
    """處理 /add 指令"""
    result = num1 + num2
    await ctx.respond(f"{num1} + {num2} = {result}")
    
# ----------------------------------------------------------------------------

# 讀取地點資訊
def get_location_json():
    try:
        with open("location.json", "r", encoding="utf-8") as f:
            locations = json.load(f)
        return [location['name'] for location in locations['locations']]
    except FileNotFoundError:
        print("找不到 'location.json' 檔案，請確認檔案存在於正確位置")
        return []

# 查詢天氣資料
def get_weather(SID):
    dataid = "O-A0001-001"
    apikey = "CWA-45F1CA8C-863A-4CD6-A3F2-45C726E486D1"
    url = f"https://opendata.cwa.gov.tw/api/v1/rest/datastore/{dataid}"
    params = {
        "Authorization": apikey,
        "format": "json",
        "stationId": SID,
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        try:
            station_data = data["records"]["Station"][0]  # 假設只返回一個站點
            obs_time = format_time(station_data["ObsTime"]["DateTime"])  # 查詢時間
            weather_elements = station_data["WeatherElement"]
            return obs_time, weather_elements
        except (KeyError, IndexError):
            return "無法解析資料，請檢查 API 回應格式", {}
    else:
        return "無法取得資料，請稍後再試", {}

def format_weather_embed(embed, weather_elements):
    """格式化天氣資訊到嵌入式內容"""
    for element, value in weather_elements.items():
        if isinstance(value, dict):  # 嵌套結構處理
            if element == "Now":  # 即時降水量
                embed.add_field(name="即時降水量", value=f"{value.get('Precipitation', '無資料')} mm", inline=True)
            elif element == "GustInfo":  # 陣風資訊
                gust_speed = value.get('PeakGustSpeed', '無資料')
                gust_time = format_time(value.get('Occurred_at', {}).get('DateTime', '無資料'))
                embed.add_field(name="最大陣風速", value=f"{gust_speed} m/s", inline=True)
                embed.add_field(name="陣風時間", value=gust_time, inline=True)
            elif element == "DailyExtreme":  # 日高低溫
                high_temp = value.get('DailyHigh', {}).get('TemperatureInfo', {}).get('AirTemperature', '無資料')
                high_time = format_time(value.get('DailyHigh', {}).get('TemperatureInfo', {}).get('Occurred_at', {}).get('DateTime', '無資料'))
                low_temp = value.get('DailyLow', {}).get('TemperatureInfo', {}).get('AirTemperature', '無資料')
                low_time = format_time(value.get('DailyLow', {}).get('TemperatureInfo', {}).get('Occurred_at', {}).get('DateTime', '無資料'))
                embed.add_field(name="日低溫", value=f"{low_temp}°C (時間: {low_time})", inline=False)
                embed.add_field(name="日高溫", value=f"{high_temp}°C (時間: {high_time})", inline=False)
        else:  # 單一數值
            embed.add_field(name=element, value=value, inline=True)

def format_time(datetime_str):
    """格式化時間字串為指定的樣式"""
    try:
        # 解析 ISO 8601 格式的時間字串
        dt = datetime.fromisoformat(datetime_str.replace("Z", "+00:00"))
        # 格式化為 `YYYY-MM-DD HH:MM:SS UTC+8`
        return dt.strftime("%Y-%m-%d %H:%M:%S UTC%z")
    except ValueError:
        return "無效時間"

# 定義指令
@bot.slash_command(name="weather_location_select", description="查找天氣")
async def choose_location(interaction: discord.Interaction, location: discord.Option(str, "選擇要查找天氣的地方", choices=get_location_json())):
    try:
        # 取得選中的地點資料
        with open("location.json", "r", encoding="utf-8") as f:
            locations = json.load(f)
        selected_location = next(loc for loc in locations['locations'] if loc['name'] == location)
        SID = selected_location["SID"]

        # 查詢天氣資料
        obs_time, weather_elements = get_weather(SID)

        # 建立嵌入式回應
        embed = discord.Embed(
            title = f"{location} 的天氣資訊",
            description = f"觀測時間：{obs_time}",
            color = discord.Color.blue(),
            timestamp = datetime.now(),
        )

        if isinstance(weather_elements, dict):
            format_weather_embed(embed, weather_elements)
        else:
            embed.description = weather_elements  # 當 weather_elements 是錯誤訊息時

        await interaction.response.send_message(embed=embed)
    except Exception as e:
        await interaction.response.send_message(f"發生錯誤：{str(e)}")
    
# ----------------------------------------------------------------------------

bot.run(getenv("TOKEN"))