import logging

from aiogram import Router
from aiogram.types import Message

from config import DEVICES
from filters.payment_type import IsClickChat
from logs.logger import DeviceLog
from services.MQTT.pub_requests import Publisher
from modules.device_control.parsers import PaymentInfoParser
from services.database.engine import session
from services.database.requests import Orders

main_rt = Router(name='main')


@main_rt.message(IsClickChat())
async def handle_click_message(message: Message):
    """
    Click payment system messages handler
    """
    data = await PaymentInfoParser.click(message.text)

    log: DeviceLog = data.get('log')
    device = data.get("device")

    if device:
        if data.get('amount'):
            command = f"PAYMENT_OK:{data.get('amount')}"
            await Publisher().command_to(device.device_id, command)
            log.info(f"Отправлена команда {command.strip()}")
            await message.reply(f"{device.device_id}: {command.strip()}")
        else:
            log.error(f"Оплата не произведена")

    async with session:
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