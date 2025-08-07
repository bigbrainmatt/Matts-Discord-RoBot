import discord
import os
from discord.ext import commands
from dotenv import load_dotenv
from database import Database

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
GUILD_ID = int(os.getenv("GUILD_ID"))

intents = discord.Intents.default()
intents.messages = True
intents.guilds = True
intents.reactions = True
intents.members = True
intents.guild_messages = True
intents.guild_reactions = True

bot = commands.Bot(command_prefix="!", intents=intents)

async def load_cogs():
    for root, dirs, files in os.walk("./cmds"):
        for file in files:
            if file.endswith(".py"):
                module = os.path.relpath(os.path.join(root, file), ".").replace(os.sep, ".")[:-3]
                await bot.load_extension(module)
                print(f"⚙️ Loaded cog: {module}")

@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")

    try:
        await bot.tree.sync()
        print("✅ Synced commands globally")
        guild = discord.Object(id=GUILD_ID)
        await bot.tree.sync(guild=guild)
        db = Database(guild.id)
        print(f"✅ Commands synchronized to guild {GUILD_ID}")
    except Exception as e:
        print(f"❌ Failed to sync commands: {e}")

    await bot.change_presence(status=discord.Status.online,
                              activity=discord.CustomActivity("Doing some shit"))

async def run_bot():
    async with bot:
        await load_cogs()
        await bot.start(TOKEN)