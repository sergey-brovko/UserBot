from pyrogram import Client
from dotenv import load_dotenv
import os

load_dotenv()


async def app():
    async with Client("my_account", os.getenv('API_ID'), os.getenv('API_HASH')) as app:
        await app.send_message("me", "Greetings from **Pyrogram**!")