# --- DEPRECATED SCRIPT ---
# This script appears to be a simplified, earlier version of the main bot (`main.py`).
# It has limited functionality and is likely no longer in use.
# It is recommended to remove this file from the project to avoid confusion.
# The main bot logic is now handled in `main.py`.

import os
from dotenv import load_dotenv
import discord
from discord.ext import commands
import logging

# Load environment variables from .env file
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
CHANNEL_ID = int(os.getenv("CHANNEL_ID_AI"))

# Configure logging
logging.basicConfig(level=logging.INFO)

# Create intents and the bot
intents = discord.Intents.default()
intents.messages = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    """
    Called when the bot is ready and connected to Discord.
    Sends a single message to a specific channel.
    """
    logging.info(f'Bot connected as {bot.user}')
    channel = bot.get_channel(CHANNEL_ID)
    if channel:
        guild = channel.guild
        role = discord.utils.get(guild.roles, name="Hamilton 10") if guild else None
        role_mention = role.mention if role else ""

        await channel.send(f"🤖 {role_mention} Hello I'm CheckinBot Don't Forget to checkin, sorry for being today 🤖")
    else:
        logging.error("The specified channel was not found.")

# This block is not strictly necessary as the bot only sends one message and exits.
# However, it keeps the bot running if you intend to add more functionality.
if __name__ == "__main__":
    bot.run(TOKEN)