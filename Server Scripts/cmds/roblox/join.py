import discord
import os
from discord.ext import commands
from dotenv import load_dotenv
from typing import List

class onUserJoinGame(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        load_dotenv()

        try:
            self.guild_id = int(os.getenv("GUILD_ID"))
            self.channel_id = int(os.getenv("ROBLOX_LOGS"))
        except (TypeError, ValueError):
            print("❌ Environment variables GUILD_ID or ROBLOX_LOGS are missing or invalid.")
            self.guild_id = None
            self.channel_id = None

    async def log_to_discord(self, userInfo: List[str]):
        if not self.guild_id or not self.channel_id:
            return False

        guild = self.bot.get_guild(self.guild_id)
        if not guild:
            return False

        channel = guild.get_channel(self.channel_id)
        if not isinstance(channel, discord.TextChannel):
            return False

        userInfo = [str(value) for value in userInfo]

        embed = discord.Embed(title="Roblox Join Log", color=discord.Color.green())
        embed.add_field(name="Username", value=userInfo[0], inline=False)
        embed.add_field(name="User ID", value=userInfo[1], inline=False)
        embed.add_field(name="Display Name", value=userInfo[2], inline=False)
        embed.add_field(name="Account Age", value=self.format_age(int(userInfo[3])), inline=False)
        embed.add_field(name="Membership Status", value="Normal" if  userInfo[4].endswith("None") else "Premium", inline=False)
        embed.add_field(name="Join Timestamp", value=userInfo[5], inline=False)
        embed.add_field(name="Server ID", value=userInfo[6], inline=False)

        await channel.send(embed=embed)
        return True

    def format_age(self, days: int) -> str:
        years = days // 365
        remaining_days = days % 365
        months = remaining_days // 30
        days_left = remaining_days % 30

        parts = []
        if years:
            parts.append(f"{years} Year{'s' if years != 1 else ''}")
        if months:
            parts.append(f"{months} Month{'s' if months != 1 else ''}")
        if days_left or not parts:
            parts.append(f"{days_left} Day{'s' if days_left != 1 else ''}")

        return ' '.join(parts)

async def setup(bot):
    await bot.add_cog(onUserJoinGame(bot))