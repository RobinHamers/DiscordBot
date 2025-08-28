import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
import logging

def get_techtalk_message_if_today(json_keyfile_path, sheet_url):
    """
    Fetches "Tech-Talk" information from a Google Sheet for the current day.

    Args:
        json_keyfile_path (str): The path to the Google Cloud service account JSON keyfile.
        sheet_url (str): The URL of the Google Sheet.

    Returns:
        str: A formatted string containing the Tech-Talk schedule for the day, or an empty string if there are no talks.
    """
    try:
        # Authorize with Google Sheets API.
        scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
        creds = ServiceAccountCredentials.from_json_keyfile_name(json_keyfile_path, scope)
        client = gspread.authorize(creds)

        # Open the Google Sheet.
        sheet = client.open_by_url(sheet_url).sheet1

        # Get headers from the second row.
        headers = sheet.row_values(2)

        # Find the index of the required columns.
        date_idx = headers.index('Date') if 'Date' in headers else -1
        learner_idx = headers.index('Learner') if 'Learner' in headers else -1
        theme_idx = headers.index('Theme') if 'Theme' in headers else -1
        voice_idx = headers.index('Voice') if 'Voice' in headers else -1
        slides_idx = headers.index('Slides') if 'Slides' in headers else -1
        body_lang_idx = headers.index('Body Language') if 'Body Language' in headers else -1

        # Fetch all records from the sheet.
        records = sheet.get_all_records(head=2)

        # Get today's date in the format used in the sheet.
        today_str = datetime.today().strftime('%-d/%-m/%y')
        
        messages = []
        for row in records:
            date_value = str(row.get(headers[date_idx], "")).strip() if date_idx != -1 else ""

            # Check if the row corresponds to today's date.
            if date_value == today_str:
                learner = row.get(headers[learner_idx], "N/A") if learner_idx != -1 else "N/A"
                theme = row.get(headers[theme_idx], "N/A") if theme_idx != -1 else "N/A"
                voice = row.get(headers[voice_idx], "N/A") if voice_idx != -1 else "N/A"
                slides = row.get(headers[slides_idx], "N/A") if slides_idx != -1 else "N/A"
                body_lang = row.get(headers[body_lang_idx], "N/A") if body_lang_idx != -1 else "N/A"

                msg = (
                    f"\n🎤 TECH-TALK ALERT 🎤\n"
                    f"Learner: {learner}\n"
                    f"Theme: {theme}\n"
                    f"Voice: {voice}\n"
                    f"Slides: {slides}\n"
                    f"Body Language: {body_lang}"
                )
                messages.append(msg)

        return "\n\n".join(messages) if messages else ""

    except Exception as e:
        logging.error(f"Error fetching Tech-Talk data: {e}")
        return ""


if __name__ == "__main__":
    # This block is for testing the script directly.
    json_keyfile_path = "discordbot.json"
    sheet_url = "https://docs.google.com/spreadsheets/d/1FLktNFlFQCHLaEnw_o_0UJDcXnpYxg2ynoZeq_b-iBQ/edit?gid=0#gid=0"

    techtalk_message = get_techtalk_message_if_today(json_keyfile_path, sheet_url)
    if techtalk_message:
        print("Tech Talk Message(s) for Today:")
        print(techtalk_message)
    else:
        print("No tech talks scheduled for today.")