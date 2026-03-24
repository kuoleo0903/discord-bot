import discord
from discord.ext import commands
from core.classes import BaseCog

class ast_cal(BaseCog):
    # 定義需要 *4 轉換的科目
    GSAT_SUBJECTS = ["國文", "英文"]
    
    @commands.slash_command(name="ast_calculate", description="分科分數計算 (國英自動轉換學測級分)")
    async def calculate(
        self,
        ctx: discord.ApplicationContext,
        chinese: discord.Option(str, "格式：科目分數*倍率 (例如: 國15*1.5)", default="0*1"),
        english: discord.Option(str, "格式：科目分數*倍率 (例如: 英15*1.5)", default="0*1"),
        math_a: discord.Option(float, "數甲 (分科倍率)", default=0),
        physics: discord.Option(float, "物理 (分科倍率)", default=0),
        chemistry: discord.Option(float, "化學 (分科倍率)", default=0),
        biology: discord.Option(float, "生物 (分科倍率)", default=0),
        history: discord.Option(float, "歷史 (分科倍率)", default=0),
        geography: discord.Option(float, "地理 (分科倍率)", default=0),
        civics: discord.Option(float, "公民 (分科倍率)", default=0),
    ):
        try:
            c_score, c_mul = chinese.split("*")
            e_score, e_mul = english.split("*")
            
            chinese = float(c_score)
            chinese_mul = float(c_mul)
            english = float(e_score)
            english_mul = float(e_mul)
        except ValueError:
            return await ctx.respond("輸入格式有誤，請使用 '分數*倍率' 格式 (例如: 國15*1.5)")
        
        """
        邏輯：
        1. 國英輸入為 0-15，自動 *4 變 60 級分。
        """
        subjects_data = {
            "國文": chinese, "英文": english, "數甲": math_a,
            "物理": physics, "化學": chemistry, "生物": biology,
            "歷史": history, "地理": geography, "公民": civics
        }

        total_weighted = 0.0
        details = []

        for name, score in subjects_data.items():
            if score > 0:
                # 判斷是否需要學測轉換
                actual_score = score * 4 if name in self.GSAT_SUBJECTS else score
                
                if name == "國文":
                    weighted = actual_score * chinese_mul
                    total_weighted += weighted
                    details.append(f"**{name}**: {actual_score} (加權後: {weighted})")
                elif name == "英文":
                    weighted = actual_score * english_mul
                    total_weighted += weighted
                    details.append(f"**{name}**: {actual_score} (加權後: {weighted})")
                else:
                    # 計算該科加權
                    weighted = 60 * score
                    total_weighted += weighted
                    details.append(f"**{name}**: 60\*{actual_score} (加權後: {weighted})")
                
                

        if not details:
            return await ctx.respond("請至少輸入一科的分數！")

        # 製作結果 Embed
        embed = discord.Embed(title="📊 分科測驗模擬計算結果", color=discord.Color.green())
        embed.description = "\n".join(details)
        embed.add_field(name="加權最高(扣除國英)", value=f"**{total_weighted:.2f}**", inline=True)
        embed.set_footer(text="註：國英已自動將學測 15 級分乘以4轉換為分科 60 級分制")

        await ctx.respond(embed=embed)

def setup(bot):
    print("✅ ast_cal Cog 已載入")
    bot.add_cog(ast_cal(bot))