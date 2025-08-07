import discord
from discord import app_commands
from discord.ext import commands
from database import Database
import dotenv

class LogSetup(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="setup_log", description="Setup your Roblox Logs")
    async def setup_log(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)

        conf = discord.Embed (
            title="Log Setup",
            description="Please select the log types you want to set up.",
            color=discord.Color.blue()
        )

        player_events = [
            discord.ui.Button(label="PlayerJoin", custom_id="player_join"),
            discord.ui.Button(label="PlayerLeave", custom_id="player_leave")
        ]
        server_events = [
            discord.ui.Button(label="ServerStart", custom_id="server_start"),
            discord.ui.Button(label="ServerShutdown", custom_id="server_shutdown"),
            discord.ui.Button(label="Heartbeat", custom_id="heartbeat"),
            discord.ui.Button(label="ScriptError", custom_id="script_error"),
            discord.ui.Button(label="PurchaseEvent", custom_id="purchase_event"),
            discord.ui.Button(label="CustomEvent", custom_id="custom_event")
        ]
        chat_events = [
            discord.ui.Button(label="ChatMessage", custom_id="chat_message"),
            discord.ui.Button(label="CommandUsed", custom_id="command_used")
        ]





async def setup(bot: commands.Bot):
    await bot.add_cog(LogSetup(bot))