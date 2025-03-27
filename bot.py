import os
import logging
import asyncio

from config import BOT_TOKEN, DEBUG
from dispatcher import bot, dp

from modules.device_control.handlers.control_devices import main_rt
from services.Excel.export_data import export_orders_to_excel
from services.MQTT.sub_requests import Listener


from services.database.engine import init_db, session
from services.database.requests import Devices


# from tests.db_tests import start_test



def start_logging():
    if DEBUG:
        logging.basicConfig(level=logging.INFO)
        return

    if not os.path.isdir('logs'):
        os.mkdir('logs')
    logging.basicConfig(
        filename=f'./logs/bot_{BOT_TOKEN.split(":")[0]}.log',
        level=logging.INFO,
        format='~%(asctime)s %(message)s',
        encoding='utf-8'
    )

def setup_routers():
    dp.include_router(main_rt)

async def set_mqtt_listeners():
    async with session:
        devices = await Devices(session).get()
        for device in devices:
            asyncio.create_task(Listener().response(device.device_id))

async def main():
    setup_routers()
    # await start_test()
    await init_db()
    # await export_orders_to_excel('2025-03-20')
    await set_mqtt_listeners()
    # await bot.send_message(-1002617742941, 'test')
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == '__main__':
    start_logging()

    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Exit')
