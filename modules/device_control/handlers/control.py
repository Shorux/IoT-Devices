from aiogram import Router
from aiogram.types import Message

from config import DEVICES
from filters.payment_type import IsClickChat
from services.MQTT.requests import MQTTRequests
from modules.device_control.parsers import PaymentInfoParser

main_rt = Router(name='main')


@main_rt.message(IsClickChat())
async def handle_click_message(message: Message):
    """
    Click payment system messages handler
    """
    data = PaymentInfoParser.click(message.text)
    device_id = data.get("device_id")

    if data.get('status') == 'Успешно подтвержден':
        if device_id in DEVICES:
            command = "LED_ON 123"
            await MQTTRequests(device_id).publish(command)
            await message.reply(f"{device_id}: {command.strip()}")
        else:
            await message.reply(f"? {device_id}")
    else:
        await message.reply("Оплата не произведена")
