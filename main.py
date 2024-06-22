import asyncio
from app.database.models import async_main
from app.handlers import app_run


async def main():
    await app_run()
    await async_main()



if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Бот выключен')
