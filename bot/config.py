from dotenv import load_dotenv
import os

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

CHANNEL_1_ID = os.getenv("CHANNEL_1_ID")
CHANNEL_1_NAME = os.getenv("CHANNEL_1_NAME")

CHANNEL_2_ID = os.getenv("CHANNEL_2_ID")
CHANNEL_2_NAME = os.getenv("CHANNEL_2_NAME")

if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN required in .env")

CHANNELS = []
if CHANNEL_1_ID:
    CHANNELS.append({
        "id": int(CHANNEL_1_ID),
        "name": CHANNEL_1_NAME or "Channel 1"
    })
if CHANNEL_2_ID:
    CHANNELS.append({
        "id": int(CHANNEL_2_ID),
        "name": CHANNEL_2_NAME or "Channel 2"
    })

if not CHANNELS:
    raise ValueError("No channels configured in .env")
