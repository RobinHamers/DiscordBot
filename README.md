# Becode Discord Bot

## Overview

The **Becode Discord Bot** is a comprehensive tool designed to support learners at Becode. It automates daily tasks, provides educational assistance, and fosters a positive learning environment. The bot leverages **Google Gemini** for intelligent and witty responses, **Discord.py** for its framework, and **APScheduler** for scheduling messages.

## Features

- **Automated Reminders**: Sends timely reminders for check-ins, check-outs, breaks, and lunch.
- **AI-Powered Assistance**: Answers questions on data science, data analysis, and Python using Google Gemini.
- **Moodle Integration**: Provides direct links to Moodle check-in/check-out pages.
- **Google Sheets Integration**: Fetches and displays daily "Tech-Talk" schedules from a Google Sheet.
- **Personalized Interactions**: Wishes users a happy birthday and responds to direct mentions with helpful information.
- **Customizable**: Easily configure channel IDs, user roles, and schedules.

## Project Structure

The project is organized into the following files:

- **`main.py`**: The main entry point of the bot. It handles Discord events, schedules tasks, and integrates with the Gemini API.
- **`sheets_utils.py`**: A utility module for fetching and parsing data from Google Sheets, specifically for the "Tech-Talk" feature.
- **`direct_discussion.py`**: A simpler, possibly deprecated, version of the bot. Its functionality is largely included in `main.py`.
- **`requirements.txt`**: A list of all the Python dependencies required to run the bot.
- **`.env.example`**: An example file for the environment variables. You should rename this to `.env` and fill in your own values.
- **`Dockerfile`**: Allows for easy containerization of the bot.
- **`LICENSE`**: The license for the project.
- **`user_chats.json`**: Stores conversation history with users to maintain context.

## Prerequisites

- Python 3.8+
- A Discord Bot Token
- A Google Gemini API Key
- A Google Cloud project with the Sheets API enabled and a service account JSON keyfile.

## Installation and Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-username/becode-discord-bot.git
   cd becode-discord-bot
   ```
2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
3. **Set up environment variables**:
   - Rename `.env.example` to `.env`.
   - Open the `.env` file and add your specific credentials.

   ```env
   DISCORD_TOKEN="your_discord_bot_token"
   CHANNEL_ID_AI="your_ai_channel_id"
   CHANNEL_ID_WEBDEV="your_webdev_channel_id"
   CHANNEL_TEST_ID="your_test_channel_id"
   GEMINI_API="your_gemini_api_key"
   # User IDs for birthday wishes
   Ali="user_id_for_ali"
   Robin="user_id_for_robin"
   Elsa="user_id_for_elsa"
   Mehdi="user_id_for_mehdi"
   ```

4. **Run the bot**:
   ```bash
   python main.py
   ```

## Commands and Usage

- **/time**: Displays the current time.
- **Mention the bot**: Mention the bot in a message to get a response.
  - Ask for the time: "Hey @bot, what time is it?"
  - Ask about Tech-Talks: "Hey @bot, what's the tech talk today?"
  - Ask a question: "Hey @bot, can you explain what a list comprehension is in Python?"
- **Direct Messages**: Send a direct message to the bot to get the current time and the time until the next event.

## Customization

- **Schedules**: Modify the `checkin_times`, `checkout_times`, `break_time`, and `lunch_time` variables in `main.py` to change the reminder schedule.
- **Birthdays**: Add or modify users in the `birthdays` dictionary in `main.py` to send birthday wishes.
- **Channels and Roles**: Change the channel IDs and role names in `main.py` to match your Discord server setup.

## Contributing

Contributions are welcome! If you have any ideas for new features or improvements, please follow these steps:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature/your-feature-name`).
3. Make your changes and commit them (`git commit -m 'Add some feature'`).
4. Push to the branch (`git push origin feature/your-feature-name`).
5. Open a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
