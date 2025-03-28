import math

from aiogram import Router
from aiogram.types import Message

from filters.payment_type import IsClickChat
from logs.logger import DeviceLog
from services.MQTT.pub_requests import Publisher
from modules.device_control.parsers import PaymentInfoParser
from services.database.engine import async_session
from services.database.requests import Orders

main_rt = Router(name='main')

def calculate(amount: float) -> int:
    if amount < 10000:
        return 0
    count = math.ceil(amount / 1000)
    return count

@main_rt.message(IsClickChat())
async def handle_click_message(message: Message):
    """
    Click payment system messages handler
    """
    data = await PaymentInfoParser.click(message.text)

    log: DeviceLog = data.get('log')
    device = data.get("device")
    amount = data.get('amount')
    if not amount:
        log.info('Оплата не произведена')

    if device:
        impulses = calculate(amount)
        if impulses:
            command = f"PAYMENT_OK:{impulses-10},ID:{data.get('transaction_id')}" if impulses > 10 else f"PAYMENT_OK,ID:{data.get('transaction_id')}"
            await Publisher().command_to(device.device_id, command)
            log.info(f"Отправлена команда {command.strip()}")
            await message.reply(f"{device.device_id}: {command.strip()}")
        else:
            log.error(f"Сумма меньше 10 тыс. сум")

    async with async_session() as session:
        orders_db = Orders(session)
        await orders_db.create(
            payment_name=data.get("payment_name"),
            transaction_id=data.get("transaction_id"),
            amount=data.get("amount"),
            date=data.get("date"),
            time=data.get("time"),
            status=data.get("status"),
            device=data.get("device"),
            log=str(log)
        )