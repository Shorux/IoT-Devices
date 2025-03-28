from io import BytesIO

import pandas as pd

from datetime import datetime, timedelta

from aiogram.types import BufferedInputFile, CallbackQuery

from services.database.models import Order
from services.database.requests import Orders
from services.database.engine import async_session


async def get_orders_excel(period, message):
    today = datetime.today().date()

    if period == "day":
        start_date, end_date = today, today
    elif period == "week":
        start_date, end_date = today - timedelta(days=today.weekday()), today
    elif period == "month":
        start_date, end_date = today.replace(day=1), today
    elif period == 'all':
        start_date, end_date = None, None
    else: return

    async with async_session() as session:
        orders_db = Orders(session)
        if period == 'all':
            orders = await orders_db.get()
        else:
            orders = await orders_db.get(where=Order.date.between(start_date, end_date))

        if not orders:
            return None

    data = [
        {
            "Название оплаты": order.payment_name,
            "ID устройства": order.device_id,
            "Сумма": order.amount,
            "Дата": order.date,
            "Время": order.time,
            "Статус": "✅ Подтверждён" if order.status else "❌ Не подтверждён",
            "Лог": order.log,
            "Создано": order.created_at
        }
        for order in orders
    ]
    df = pd.DataFrame(data)

    # Подсчёты
    total_orders = len(orders)
    confirmed_orders = sum(1 for order in orders if order.status)
    total_amount = sum(order.amount for order in orders if order.amount)

    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        workbook = writer.book

        # Страница с заказами
        df.to_excel(writer, sheet_name='Заказы', index=False)
        worksheet = writer.sheets['Заказы']

        # Форматы
        bold_format = workbook.add_format({'bold': True, 'align': 'center'})
        money_format = workbook.add_format({'num_format': '#,##0.00'})
        date_format = workbook.add_format({'num_format': 'yyyy-mm-dd'})
        time_format = workbook.add_format({'num_format': 'hh:mm:ss'})
        status_format_confirmed = workbook.add_format({'bold': True, 'font_color': 'green'})
        status_format_pending = workbook.add_format({'bold': True, 'font_color': 'red'})

        # Применение форматов
        worksheet.set_row(0, None, bold_format)
        worksheet.set_column('A:A', 20)  # Название оплаты
        worksheet.set_column('B:B', 12)  # ID устройства
        worksheet.set_column('C:C', 10, money_format)  # Сумма
        worksheet.set_column('D:D', 12, date_format)  # Дата
        worksheet.set_column('E:E', 10, time_format)  # Время
        worksheet.set_column('F:F', 15)  # Статус
        worksheet.set_column('G:G', 40)  # Лог
        worksheet.set_column('H:H', 18, date_format)  # Создано

        # Применение цветового форматирования для статусов
        for row_num, status in enumerate(df['Статус'], start=1):
            fmt = status_format_confirmed if "Подтверждён" in status else status_format_pending
            worksheet.write(row_num, 5, status, fmt)

        # Страница с итогами
        summary_data = {
            "Всего заказов": [total_orders],
            "Подтверждённые заказы": [confirmed_orders],
            "Общая сумма": [total_amount]
        }
        df_summary = pd.DataFrame(summary_data)
        df_summary.to_excel(writer, sheet_name='Итог', index=False)

        # Оформляем итоги
        summary_ws = writer.sheets['Итог']
        summary_ws.set_row(0, None, bold_format)
        summary_ws.set_column('B:B', 10, money_format)  # Общая сумма

    output.seek(0)

    excel = BufferedInputFile(output.getvalue(), filename=f"{period}_orders.xlsx")

    if excel:
        await message.answer_document(excel)
    else:
        await message.answer('Нет данных')
    await message.delete()
