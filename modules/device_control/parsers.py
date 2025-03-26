import re

from datetime import time, date


class PaymentInfoParser:
    @staticmethod
    def click(text: str) -> dict | None:
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
        amount_match = re.search(r"🇺🇿 ([\d\.]+) сум", text)
        date_time_match = re.search(r"🕓 (\d{2}:\d{2}:\d{2}) (\d{2}\.\d{2}\.\d{4})", text)

        data = {
            'device_id': int(device_match.group(1)) if device_match else None,
            'transaction_id': int(order_id_match.group(1)) if order_id_match else None,
            'amount': float(amount_match.group(1)) if amount_match else None,
            'time': time.strftime(date_time_match.group(1), '%H:%M:%S')  if date_time_match else None,
            'date': date.strftime(date_time_match.group(2), '%d.%m.%Y')  if date_time_match else None,
            'status': text.split('\n')[-1][2:],
            'payment_name': 'Click'
        }

        return data if all(value is not None for value in data.values()) else None
