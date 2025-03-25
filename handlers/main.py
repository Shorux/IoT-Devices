from aiogram import Router
from aiogram.filters import Command

main_rt = Router()

@main_rt.message(Command('send_request'))
async def send_request(message):
    await message.answer('Отправьте запрос на обработку')
