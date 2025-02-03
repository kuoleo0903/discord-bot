import discord
from discord.errors import NotFound
import requests
from core.classes import Cog_Extension


AUTHORIZED_USER_ID = 439814891176460299  # 替換成你的 Discord 使用者 ID

class ping(Cog_Extension):
    @discord.bot.slash_command()
    async def ping(ctx):
        await ctx.send(f'{round(bot.latency * 1000)} (ms)')

    # ----------------------------------------------------------------------------

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

    @discord.bot.slash_command(self, description="取得伺服器的對外 IP")
    async def get_server_ip(ctx):
        """處理 /get_server_ip 指令"""
        if ctx.author.id == AUTHORIZED_USER_ID:
            ip = self.get_public_ip()
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

    @discord.bot.slash_command(description="查看機器人是否上線")
    async def check_online(ctx):
        """處理 /check_online 指令"""
        await ctx.respond("機器人正常運行中！")
        
def setup(bot):
    bot.add_cog(ping(bot))