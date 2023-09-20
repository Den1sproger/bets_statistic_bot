from aiogram.types import (ReplyKeyboardMarkup,
                           KeyboardButton)


main_kb = ReplyKeyboardMarkup(
    resize_keyboard=True,
    keyboard=[
        [KeyboardButton('Голосование')],
        [KeyboardButton('Статистика')],
        [KeyboardButton('Подписаться')]
    ]
)