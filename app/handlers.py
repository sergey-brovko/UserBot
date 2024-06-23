from pyrogram import Client, filters
from pyrogram.errors import UserDeactivated, UserBlocked
import app.database.requests as rq
from datetime import timedelta
from dotenv import load_dotenv
import asyncio
import os

load_dotenv()


async def app_run():
    app = Client("my_account", os.getenv('API_ID'), os.getenv('API_HASH'))

    @app.on_message(filters.text & filters.private)
    async def echo(_, message):
        me = await app.get_me()
        if me.id != message.from_user.id:
            await rq.set_user(message.from_user.id)

    async def check_triggers(user_id: int, phrase: str) -> bool:
        phrase = phrase.lower()
        async for message in app.get_chat_history(user_id):
            if (await rq.set_trigger_history(user_id=user_id, message_id=message.id) and message.outgoing
                    and (phrase in message.text.lower())):
                return True
            return False

    async def send_message(users: list, text_message: str) -> None:
        for user in users:
            if not await check_triggers(user.id, 'ожидать'):
                try:
                    await app.send_message(user.id, text_message)
                    await rq.update_send_message(user.id)
                except (UserDeactivated, UserBlocked) as e:
                    print(e)
                    await rq.update_status(user.id, "dead")
            else:
                await rq.update_status(user.id, "finished")

    async def filter_users_by_step(*args: tuple[timedelta, str]) -> None:
        for i, arg in enumerate(args):
            users = await rq.get_users_by_step(arg[0], i)
            if users:
                await send_message(users, arg[1])

    async with app:
        while True:
            await filter_users_by_step((timedelta(minutes=6), 'Text1'),
                                       (timedelta(minutes=39), 'Text2'),
                                       (timedelta(days=1, hours=2), 'Text3'))
            await asyncio.sleep(5)
