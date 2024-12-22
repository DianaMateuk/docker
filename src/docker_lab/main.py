from asyncio import run, sleep
from logging import basicConfig, INFO, error

from database.database import init_db
from sync.sync import sync


async def start():
    await init_db()
    while True:
        try:
            await sync()
            await sleep(5)
        except Exception as e:
            error(e)
            await sleep(10)

if __name__ == '__main__':
    basicConfig(level=INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    run(start())
