from pyrogram import Client, filters, errors
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


async def check_triggers(user_id: int, phrase: str) -> bool:
    phrase = phrase.lower()
    async for message in app.get_chat_history(user_id):
        if (await rq.set_trigger_history(user_id=user_id, message_id=message.id) and message.outgoing
                and (phrase in message.text.lower())):
            return True
        return False


async def send_message(users: list, text_message: str, sent_message: str, last_message: bool = False) -> None:

    for user in users:
        if not await check_triggers(user.id, 'ожидать'):
            try:
                if user.status == 'alive' and user.send_message != sent_message:
                    await app.send_message(user.id, text_message)
                    await rq.update_send_message(user.id, sent_message)
                    if last_message:
                        await rq.update_status(user.id, "finished")
            except errors.UserDeactivated as e:
                print(e)
                await rq.update_status(user.id, "dead")
        else:
            await rq.update_status(user.id, "finished")


async def filter_users_by_step():
    step1, step2, step3 = timedelta(minutes=6), timedelta(minutes=45), timedelta(days=1, hours=2, minutes=45)
    users3 = await rq.get_users_by_step(step3, step3+timedelta(days=1))
    users2 = await rq.get_users_by_step(step2, step3)
    users1 = await rq.get_users_by_step(step1, step2)
    if users3:
        await send_message(users3, 'Текст3', 'third_message', True)
    if users2:
        await send_message(users2, 'Текст2', 'second_message')
    if users1:
        await send_message(users1, 'Текст1', 'first_message')


async def app_run():
    async with app:
        while True:
            await filter_users_by_step()
            await asyncio.sleep(5)

app.run(app_run())
