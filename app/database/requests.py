from app.database.models import async_session
from app.database.models import User, Trigger
from sqlalchemy import select, update, delete, func
import datetime


# current_time = datetime.datetime.now()
# print(current_time)
async def set_user(tg_id: int) -> None:
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.id == tg_id))

        if not user:
            session.add(User(id=tg_id, created_at=datetime.datetime.now(), status='alive'))
            await session.commit()


async def get_users_by_step(step: datetime.timedelta):
    async with async_session() as session:
        return await session.scalars(select(User).where((User.created_at+step) <= datetime.datetime.now()))


async def set_trigger_history(user_id: int, message_id: int) -> bool:
    async with async_session() as session:
        trigger = await session.scalar(select(Trigger).where(Trigger.user_id == user_id).where(Trigger.message_id ==
                                                                                               message_id))

        if not trigger:
            session.add(Trigger(user_id=user_id, message_id=message_id))
            await session.commit()
            return True
        else:
            return False


# async def get_trigger_history(message_id: int):
#     async with async_session() as session:
#         return await session.scalar(select(Trigger).where(Trigger.id == message_id))
