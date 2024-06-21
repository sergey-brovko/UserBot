import asyncio
from app.database.models import async_main
from app.app import app


async def main():
    await async_main()
    await app()

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Бот выключен')