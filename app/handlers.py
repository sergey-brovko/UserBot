from pyrogram import Client, filters
import app.database.requests as rq
from datetime import timedelta
from dotenv import load_dotenv
import asyncio
import os

load_dotenv()

app = Client("my_account", os.getenv('API_ID'), os.getenv('API_HASH'))


@app.on_message(filters.text & filters.private)
async def echo(_, message):
    await rq.set_user(message.from_user.id)
    # await message.reply(message)


async def check_triggers(user_id: int, phrase: str):
    phrase = phrase.lower()
    async for message in app.get_chat_history(user_id):
        if (await rq.set_trigger_history(user_id=user_id, message_id=message.id) and message.outgoing
                and (phrase in message.text.lower())):
            return True
        return False


async def send_message():
    step = timedelta(minutes=10)
    users = await rq.get_users_by_step(step)
    for user in users:
        if await check_triggers(user.id, 'ожидать'):
            await app.send_message(user.id, "Text")
            print(f"Send Text for {user.id}")


async def app_run():
    async with app:
        while True:
            await send_message()
            await asyncio.sleep(10)



app.run(app_run())
