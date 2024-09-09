import os
import json
import requests
from telebot import TeleBot
from telebot import types
from dotenv import load_dotenv
import messages
import schedule
import threading
import time
from openai import OpenAI
import logging
from pydub import AudioSegment
from utils import habits_tools

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = TeleBot(token=BOT_TOKEN)
client = OpenAI()

# Set your own logging level (adjust as needed)
logging.basicConfig(level=logging.INFO)

# Configure logging to save logs to a file
log_file = 'bot_log.log'
logging.basicConfig(
    level=logging.DEBUG,  # Log level
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',  # Log format
    handlers=[
        logging.FileHandler(log_file),  # Log to file
        logging.StreamHandler()  # Also log to console (optional)
    ]
)


def send_hi_message(chat_id):
    bot.send_message(chat_id, "Hi")


def schedule_daily_message(chat_id):
    schedule.every().day.at("20:13").do(send_hi_message, chat_id=chat_id)
    while True:
        schedule.run_pending()
        time.sleep(1)


@bot.message_handler(commands=["start"])
def handle_start_command(message: types.Message):
    bot.send_message(
        message.chat.id,
        messages.start_text,
        parse_mode="HTML",
    )
    # schedule.every(5).seconds.do(send_hi_message, message.chat.id).tag(message.chat.id)
    schedule.every().day.at("20:24").do(send_hi_message, message.chat.id).tag(message.chat.id)
    # Start the thread to schedule the daily message
    # thread = Thread(target=schedule_daily_message, args=(message.chat.id,))
    # thread.start()


@bot.message_handler(commands=["help"])
def handle_help_command(message: types.Message):
    bot.send_message(
        message.chat.id,
        messages.help_text,
    )


def preprocess_voice_message(message: types.Message):
    # Get the file ID of the voice message
    file_info = bot.get_file(message.voice.file_id)
    # Download the voice message from Telegram's servers
    audio_file_path = f"https://api.telegram.org/file/bot{bot.token}/{file_info.file_path}"
    downloaded_file = requests.get(audio_file_path)

    # Save the file locally
    with open("audio_messages/audio.ogg", "wb") as new_file:
        new_file.write(downloaded_file.content)

    audio = AudioSegment.from_ogg("audio_messages/audio.ogg")
    audio.export("audio_messages/audio.mp3", format="mp3")


def extract_habits(text):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": [
                    {
                        "type": "text",
                        "text": "You are a professional assistant for tracking habits and writing a daily diary. You "
                                "will receive a transcription of a human's day based on their voice messages. From "
                                "this transcription, extract the information. Ensure that the diary is concise and "
                                "captures the main events of the day."
                    }
                ]
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": text
                    }
                ]
            }
        ],
        temperature=1,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
        tools=habits_tools,
        response_format={
            "type": "text"
        }
    )

    extraction = response.choices[0].message.tool_calls[0].function.arguments

    try:
        response_dict = json.loads(extraction)
        return json.dumps(response_dict, indent=4, ensure_ascii=False)
    except json.JSONDecodeError:
        return {"error": "Failed to parse response as JSON", "raw_response": extraction}




@bot.message_handler(content_types=['voice'])
def handle_help_command(message: types.Message):
    logging.info(f"Get audio message")
    preprocess_voice_message(message)

    audio_file = open("audio_messages/audio.mp3", "rb")

    transcription = client.audio.transcriptions.create(
        model="whisper-1",
        file=audio_file
    )
    if transcription:
        logging.info(f"Successfully transcript")

    extracted_habits = extract_habits(transcription.text)
    if extracted_habits:
        logging.info(f"Successfully extracted")

    bot.send_message(
        message.chat.id,
        transcription.text,
    )

    bot.send_message(
        message.chat.id,
        extracted_habits,
    )


if __name__ == "__main__":
    logging.info(bot.get_me())
    threading.Thread(target=bot.infinity_polling, name='bot_infinity_polling', daemon=True).start()
    while True:
        schedule.run_pending()
        time.sleep(1)
    # bot.infinity_polling(skip_pending=True)
