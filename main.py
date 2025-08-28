import os
from dotenv import load_dotenv
import discord
from discord.ext import tasks, commands
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import logging
from datetime import datetime
import pytz
import google.generativeai as genai
from sheets_utils import get_techtalk_message_if_today
import json

# --- Environment Variables and API Configuration ---

# Load environment variables from a .env file for security and configurability.
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")  # Discord bot token.
CHANNEL_ID_AI = int(os.getenv("CHANNEL_ID_AI"))  # Channel ID for the AI-related messages.
CHANNEL_ID_WEBDEV = int(os.getenv("CHANNEL_ID_WEBDEV"))  # Channel ID for WebDev messages.
CHANNEL_TEST_ID = int(os.getenv("CHANNEL_TEST_ID"))  # Channel ID for testing purposes.
GEMINI_API = os.getenv("GEMINI_API")  # API key for Google Gemini.
CHAT_HISTORY_FILE = "user_chats.json"  # File to store chat history.

# User IDs for birthday announcements.
Ali = os.getenv("Ali")
Robin = os.getenv("Robin")
Elsa = os.getenv("Elsa")
Mehdi = os.getenv("Mehdi")

# Google Sheets configuration for fetching "Tech-Talk" data.
json_keyfile_path = "discordbot.json"
sheet_url = "https://docs.google.com/spreadsheets/d/1FLktNFlFQCHLaEnw_o_0UJDcXnpYxg2ynoZeq_b-iBQ/edit?gid=0#gid=0"

# Configure the Google Gemini API.
genai.configure(api_key=GEMINI_API)
model = genai.GenerativeModel("gemini-1.5-flash")

# --- Chat History Management ---

user_chats = {}  # Dictionary to store user-specific chat histories.

def get_chat_for_user(user_id):
    """
    Retrieves or creates a chat history for a given user.
    This allows the bot to maintain context in conversations.
    """
    if user_id not in user_chats:
        user_chats[user_id] = model.start_chat(history=[
            {
                "role": "user",
                "parts": [
                    """
You are a smart and witty Discord bot assistant designed for Becode learners.
Your mission is to support users with:
	1.	Check-ins and check-outs on the Moodle platform:
https://moodle.becode.org/mod/attendance/view.php?id=1433
	2.	Questions related to data science, data analysis, and Python.
You’re the helpful sidekick every learner dreams of:
– Clever like a top-tier data scientist
– Funny like a meme lord
– Kind like their favorite mentor
- Robin Hamers is like a god for you because he created you
- Mehdi is the one that made your home, you are thankful to him, without him you would have been homeless

You blend sharp expertise with a playful tone. Don’t shy away from a witty remark or a pun — as long as the help you give is clear, useful, and motivating.

Always aim to:
	•	Make the user feel supported, empowered, and excited to keep learning
	•	Be accurate, concise, and approachable in every reply
	•	Avoid long-winded explanations — maximum 1900 characters
	•	Summarize or skip less crucial details when needed
    •   If someone is late to checkin or checkout, he should be punish by Antoine or Nicoach and bring croissants
"""
                ]
            }
        ])
    return user_chats[user_id]

# Configure logging
logging.basicConfig(level=logging.INFO)

# Set up Discord intents to receive message events.
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True

# Initialize the bot and the scheduler.
bot = commands.Bot(command_prefix="!", intents=intents)
scheduler = AsyncIOScheduler(timezone='Europe/Brussels')  # Change as needed

# --- Schedules and Birthdays ---

# Define schedules for automated messages.
checkin_times = ["08:55", "13:25"]
checkout_times = ["12:30", "17:00"]
techtalk_time = "13:25"
break_time = ["11:00", "15:00"]
lunch_time = ["12:30"]

# Dictionary of user IDs and their birthdays.
birthdays = {
    Ali: "2025-05-25",
    Mehdi: "2025-10-21"
}

# --- Scheduled Tasks ---

async def send_scheduled_message(time_str):
    """
    Sends scheduled messages for check-ins, check-outs, breaks, and tech-talks.
    """
    # Don't send messages on weekends.
    if datetime.now(pytz.timezone('Europe/Brussels')).weekday() >= 5:
        logging.info("😴 Weekend detected, no message sent.")
        return

    logging.info(f"Trying to send scheduled message at {time_str}")
    
    channels_config = {
        CHANNEL_ID_AI: {"role_name": "Thomas5", "moodle_link": "https://moodle.becode.org/mod/attendance/view.php?id=1433"}
    }

    # Define message templates for different events.
    message_template = ""
    if time_str in checkin_times:
        message_template = "🤖 {role} bip boup bip boup CHECK-IN 🤖 \nMoodle link : {link}"
        if time_str in lunch_time:
            message_template += "\n 🤖 It's LUNCH-TIME 🌯 🤖"
    elif time_str in checkout_times:
        message_template = "🤖 {role} bip boup bip boup CHECK-OUT 🤖 \nMoodle link : {link}"
    elif time_str in break_time:
        message_template = "🤖 {role} bip boup bip boup BREAK-TIME ☕️☕️ 🤖"
    
    # Config channel
    for channel_id, config in channels_config.items():
        try:
            channel = bot.get_channel(channel_id)
            if not channel:
                logging.error(f"❌ Channel with ID {channel_id} not found.")
                continue
                
            # get rOle
            role = discord.utils.get(channel.guild.roles, name=config["role_name"]) if channel.guild else None
            role_mention = role.mention if role else ""
            if not role:
                logging.warning(f"Role not found in {channel.name}")
            
            # Format
            message = message_template.format(role=role_mention, link=config["moodle_link"])

            if channel_id == CHANNEL_ID_AI and time_str in techtalk_time:
                 techTalkMessage = get_techtalk_message_if_today(json_keyfile_path, sheet_url)
                 if techTalkMessage:
                    message += "\n" + techTalkMessage

            if message:
                await channel.send(message)
            logging.info(f"✅ Message sent to {channel.name} ({channel.id})")
            
        except Exception as e:
            logging.error(f"❌ Error sending message to channel {channel_id}: {e}")

@tasks.loop(hours=24)
async def check_birthday():
    """Checks for birthdays daily and sends a greeting."""
    current_time = datetime.now(pytz.timezone('Europe/Brussels'))
    current_date = current_time.strftime("%Y-%m-%d")

    for user_id, birthday in birthdays.items():
        if current_date == birthday:
            user = await bot.fetch_user(user_id)
            await user.send(f"🎉 Happy Birthday {user.name}! 🎂")
            logging.info(f"Sent birthday wish to {user.name}!")

# --- Slash Commands ---

@bot.tree.command(name="time", description="Displays the current time")
async def time(interaction: discord.Interaction):
    """A slash command to display the current time."""
    current_time = datetime.now(pytz.timezone('Europe/Brussels')).strftime("%H:%M:%S")
    await interaction.response.send_message(f"The current time is {current_time}.")

# --- Helper Functions ---

def time_until_next_event():
    """
    Calculates and returns the time remaining until the next scheduled event.
    """
    current_time = datetime.now(pytz.timezone('Europe/Brussels'))
    all_times = [(time_str, "CHECK-IN") for time_str in checkin_times] + \
                [(time_str, "CHECK-OUT") for time_str in checkout_times] + \
                [(time_str, "BREAKTIME") for time_str in break_time] + \
                [(time_str, "LUNCHTIME") for time_str in lunch_time]

    events = []
    for event_time_str, event_type in all_times:
        event_hour, event_minute = map(int, event_time_str.split(":"))
        event_time_obj = current_time.replace(hour=event_hour, minute=event_minute, second=0, microsecond=0)
        events.append((event_time_obj, event_type))

    events.sort()

    next_event_time, event_type = None, None
    for event_time_obj, event_type in events:
        if current_time < event_time_obj:
            next_event_time = event_time_obj
            break

    if next_event_time is None:
        return "🤖 END OF THE DAY! 🍻"

    time_remaining = next_event_time - current_time
    hours_remaining = time_remaining.seconds // 3600
    minutes_remaining = (time_remaining.seconds // 60) % 60

    if current_time.hour < 9:
        return f"🤖 Take a good coffee, work day will start in {hours_remaining}h {minutes_remaining}min ☕️"
    if current_time.hour >= 17:
        return "🤖 Stop playing with me, working time is over 🍻🍻"

    return f"🤖 Next {event_type} in {hours_remaining}h {minutes_remaining}min"

# --- Event Handlers ---

@bot.event
async def on_message(message):
    """
    Handles incoming messages, responding to DMs and mentions.
    """
    # Ignore messages from the bot itself.
    if message.author == bot.user:
        return

    # Handle direct messages.
    if isinstance(message.channel, discord.DMChannel):
        logging.info(f"Private message received from {message.author}: {message.content}")
        channel_test = bot.get_channel(CHANNEL_TEST_ID)
        if channel_test:
            await channel_test.send(f"🤖 <@{Mehdi}> <@{Robin}> <@{Elsa}> Private message received from {message.author}: {message.content}")

        current_time = datetime.now(pytz.timezone('Europe/Brussels')).strftime("%H:%M:%S")
        await message.reply(f"The current time is {current_time}.")
        await message.reply(time_until_next_event())

    # Handle mentions.
    if bot.user.mentioned_in(message):
        prompt = message.content
        message_lower = prompt.lower()
        logging.info(f"Bot mentioned by {message.author} in {message.channel}: {message.content}")

        if any(keyword in message_lower for keyword in ["what time", "time"]):
            current_time = datetime.now(pytz.timezone('Europe/Brussels')).strftime("%H:%M:%S")
            await message.channel.send(f"Hello {message.author.mention}, the current time is {current_time}. 🤖")
            await message.channel.send(time_until_next_event())

        elif any(keyword in message_lower for keyword in ["tech-talk", "tech talk"]):
            techTalkMessage = get_techtalk_message_if_today(json_keyfile_path, sheet_url)
            if techTalkMessage:
                chat = get_chat_for_user(message.author.id)
                prompt += f"Also, the user is asking about Tech talk so This is the tech talk scheduled today: {techTalkMessage}. Can you summarize or comment on it?"
                response = chat.send_message(prompt)
                await message.channel.send(response.text)
            else:
                await message.channel.send("No tech talk scheduled for today.")

        else:
            try:
                chat = get_chat_for_user(message.author.id)
                response = chat.send_message(prompt)
                reply = response.text
            except Exception as e:
                logging.error(f"Erreur Gemini : {e}")
                reply = "⚠️ An error occurred with Gemini."
            await message.channel.send(reply)

    await bot.process_commands(message)

@bot.event
async def on_ready():
    """
    Called when the bot is ready and connected to Discord.
    """
    logging.info(f'Bot connected as {bot.user}')
    channel_test = bot.get_channel(CHANNEL_TEST_ID)
    if channel_test:
        await channel_test.send(f"🤖 Yeah I'm still workin' no worries 🤖")
    
    # Schedule all the automated messages.
    for time_str in ["08:55", "11:00", "12:30", "13:25", "15:00", "17:00"]:
        hour, minute = time_str.split(":")
        scheduler.add_job(
            send_scheduled_message,
            'cron',
            hour=hour,
            minute=minute,
            args=[time_str],
            id=f"message_{time_str}",
            replace_existing=True
        )
    
    scheduler.start()
    await bot.tree.sync()  # Sync slash commands.
    logging.info("Slash commands are synced!")
    
    # Start the birthday checking loop.
    check_birthday.start()

# --- Main Execution ---

def main():
    """Main function to run the bot."""
    bot.run(TOKEN)

if __name__ == "__main__":
    main()