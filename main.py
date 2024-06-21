import asyncio
from app.database.models import async_main
from app.handlers import app_run, check_triggers


async def main():
    await async_main()
    # await app_run()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Бот выключен')
