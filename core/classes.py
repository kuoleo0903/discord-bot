import discord

class Cog_Extension(discord.slash_command.Cog):
    def __init__(self, bot):
        self.bot = bot