import discord
from discord.ext import commands
from core.classes import BaseCog
from os import getenv
class ReportModal(discord.ui.Modal):
    def __init__(self, bot, *args, **kwargs) -> None:
        self.bot = bot
        super().__init__(*args, **kwargs)

        # 添加表單欄位
        self.add_item(discord.ui.InputText(
            label="機器人問題回報",
            placeholder="請輸入您的問題...",
            max_length=100
        ))
        
        self.add_item(discord.ui.InputText(
            label="詳細內容",
            placeholder="請詳細描述問題發生的經過...",
            style=discord.InputTextStyle.long, # 設定為長文本
            min_length=10,
            max_length=2000
        ))

    async def callback(self, interaction: discord.Interaction):
        """當使用者點擊送出後的處理邏輯"""
        # 回報頻道
        REPORT_CHANNEL_ID = int(getenv("REPORT_CHANNEL_ID"))
        channel = self.bot.get_channel(REPORT_CHANNEL_ID)

        # 建立回報 Embed
        embed = discord.Embed(
            title="新的問題回報", 
            color=discord.Color.orange(),
            timestamp=discord.utils.utcnow()
        )
        embed.add_field(name="標題", value=self.children[0].value, inline=False)
        embed.add_field(name="內容描述", value=self.children[1].value, inline=False)
        embed.set_footer(text=f"回報者: {interaction.user.name} ({interaction.user.id})")
        
        if interaction.user.avatar:
            embed.set_thumbnail(url=interaction.user.avatar.url)

        # 發送至管理頻道並回覆使用者
        if channel:
            await channel.send(embed=embed)
            await interaction.response.send_message("回報已送出，謝謝你的回饋！", ephemeral=True)
        else:
            # 如果找不到頻道，直接回覆在當前對話（作為備案）
            await interaction.response.send_message("回報頻道設定錯誤，請聯繫管理員。", ephemeral=True)

# 定義 Cog
class ProblemReport(BaseCog):
    @commands.slash_command(description="開啟問題回報表單")
    async def problem_report(self, ctx: discord.ApplicationContext):
        """處理 /problem_report 指令"""
        # 發送表單
<<<<<<< HEAD
        modal = ReportModal(bot=self.bot, title="問題回報表單")
=======
        modal = ReportModal(title="問題回報表單")
>>>>>>> 417bea3 (docker add)
        await ctx.send_modal(modal)

def setup(bot):
    # print("✅ ProblemReport Cog 已載入")
    bot.add_cog(ProblemReport(bot))