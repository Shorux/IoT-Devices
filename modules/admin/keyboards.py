from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

report_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='День', callback_data='day')],
        [InlineKeyboardButton(text='Неделя', callback_data='week')],
        [InlineKeyboardButton(text='Месяц', callback_data='month')],
        [InlineKeyboardButton(text='Всё время', callback_data='all')]
    ]
)
