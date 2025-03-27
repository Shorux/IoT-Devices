import logging
import re

from datetime import datetime

from services.database.engine import session
from services.database.requests import Devices
from logs.logger import DeviceLog


def is_valid_data(data: dict, log: DeviceLog) -> DeviceLog:
    is_has_none = False

    for key, value in data.items():
        if value is None:
            log.error(f"Нет значения для {key}")
            is_has_none = True

    log.info('Не хватает данных, команда не отправлена' if is_has_none else 'Все данные получены')

    return log


class PaymentInfoParser:
    @staticmethod
    async def click(text: str) -> dict:
        """
        Образец значения параметра text:
        🟢 AKRAMOV D.A. Аппарат 2 (69569)
        🆔 3976710821
        📱 +998*****5345
        💳 860003******2146
        🇺🇿 100.20 сум
        🕓 15:53:26 20.03.2025
        ✅ Успешно подтвержден
        """
        device_match = re.search(r"Аппарат\s+(\d+)", text)
        order_id_match = re.search(r"🆔 (\d+)", text)
        amount_match = re.search(r"🇺🇿 (\d+)", text)
        date_time_match = re.search(r"🕓 (\d{2}:\d{2}:\d{2}) (\d{2}\.\d{2}\.\d{4})", text)
        device_id = int(device_match.group(1)) if device_match else None
        date = datetime.strptime(date_time_match.group(2), '%d.%m.%Y')  if date_time_match else None
        time = datetime.strptime(date_time_match.group(1), '%H:%M:%S')  if date_time_match else None

        log = DeviceLog(
            message=f'Получен чек в {datetime.now().strftime("%d.%m.%Y %H:%M:%S")}',
            device_id=device_id,
        )

        async with session:
            device = await Devices(session).get(device_id) if device_id else None
            if not device:
                log.info(f'В списке нет устройства под id: {device_id}')

        data = {
            'device': device,
            'transaction_id': int(order_id_match.group(1)) if order_id_match else None,
            'amount': int(amount_match.group(1)) if amount_match else None,
            'time': time,
            'date': date,
            'status': text.split('\n')[-1][2:] == 'Успешно подтвержден',
            'payment_name': 'Click'
        }

        log = is_valid_data(data, log)
        data['log'] = log

        return data
