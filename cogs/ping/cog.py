import discord
import requests
from discord.ext import commands
from discord.errors import NotFound
from core.classes import BaseCog
from os import getenv

AUTHORIZED_USER_ID = int(getenv("AUTHORIZED_USER_ID"))  # 授權使用者 ID

class Ping(BaseCog):
    @commands.slash_command(description="查看機器人是否上線")
    async def check_online(self, ctx):
        await ctx.respond("機器人正常運行中！")

    @commands.slash_command(description="取得伺服器的對外 IP")
    async def get_server_ip(self, ctx):
        """處理 /get_server_ip 指令"""
        if ctx.author.id == AUTHORIZED_USER_ID:
            ip = self.get_public_ip()
            try:
                if ctx.channel.type == discord.ChannelType.private:
                    await ctx.respond(f"伺服器的對外 IP 是：{ip}")
                else:
                    await ctx.author.send(f"伺服器的對外 IP 是：{ip}")
                    await ctx.respond("已將伺服器 IP 發送至你的私訊！", ephemeral=True)
            except NotFound:
                await ctx.respond("交互過期或無效，請重新執行命令。")
        else:
            await ctx.respond("你無權使用此指令。", ephemeral=True)

    def get_public_ip(self):
        """從外部 API 獲取伺服器的對外 IP"""
        try:
            response = requests.get("https://api.ipify.org?format=text")
            if response.status_code == 200:
                return response.text
            else:
                return "無法取得 IP，請稍後再試"
        except Exception as e:
            return f"發生錯誤: {e}"

def setup(bot):
    bot.add_cog(Ping(bot))