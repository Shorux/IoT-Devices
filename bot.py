import os
import sys
import logging
import asyncio

from config import BOT_TOKEN, DEBUG
from dispatcher import bot, dp

from handlers.main import main_rt
from services.MQTT.requests import MQTTRequests


# from data.models import init_db
# from tests.db_tests import start_test



def start_logging():
    if DEBUG:
        logging.basicConfig(level=logging.INFO)
        return

    if not os.path.isdir('logs'):
        os.mkdir('logs')
    logging.basicConfig(
        filename=f'./logs/bot_{BOT_TOKEN.split(":")[0]}.log',
        level=logging.WARNING,
        format='~%(asctime)s %(message)s'
    )

def setup_routers():
    dp.include_router(main_rt)

async def main():
    setup_routers()
    # await start_test()
    # await init_db()
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == '__main__':
    start_logging()

    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Exit')
