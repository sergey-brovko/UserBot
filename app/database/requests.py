from app.database.models import async_session
from app.database.models import User, Trigger
from sqlalchemy import select, update, delete, func
import datetime


async def set_user(tg_id: int) -> None:
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.id == tg_id))

        if not user:
            session.add(User(id=tg_id, created_at=datetime.datetime.now(), status='alive',
                        status_updated_at=datetime.datetime.now(), send_message='not_send'))
            await session.commit()


async def update_status(tg_id: int, status: str) -> None:
    async with async_session() as session:
        await session.execute(update(User).where(User.id == tg_id).values(status=status).values(status_updated_at=datetime.datetime.now()))
        await session.commit()


async def update_send_message(tg_id: int, send_message: str) -> None:
    async with async_session() as session:
        await session.execute(update(User).where(User.id == tg_id).values(send_message=send_message))
        await session.commit()


async def get_users_by_step(step: datetime.timedelta, next_step: datetime.timedelta) -> list:
    async with async_session() as session:
        return await session.scalars(select(User).where((User.created_at+step) <=
                                                        datetime.datetime.now()).where((User.created_at+next_step) >
                                                                                       datetime.datetime.now()))


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

