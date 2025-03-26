import re
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message

from config import DEVICE_NAME
from filters.handler_filters import IsCheck
from services.MQTT.requests import MQTTRequests

main_rt = Router(name='main')

SERIAL_PORTS = [1, 2]

@main_rt.message(Command('start'))
async def start(message: Message):
    await message.answer("Hi! /led_on or /led_off")


@main_rt.message(IsCheck())
async def handle_message(message: Message):
    if message.chat.id != -1002617742941:
    # if message.chat.id == -1002617742941:
        text = message.text
        match = re.search(f"{DEVICE_NAME}\s+(\d+)", text)

        if match:
            aparat_number = int(match.group(1))

            if aparat_number in SERIAL_PORTS:
                command = "LED_ON 123"
                await MQTTRequests(aparat_number).publish(command)
                await message.reply(f"{aparat_number}: {command.strip()}")
            else:
                await message.reply(f"?{aparat_number}")
        else:
            await message.reply("?")

