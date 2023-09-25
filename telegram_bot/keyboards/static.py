from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton


main_kb = ReplyKeyboardMarkup(
    resize_keyboard=True,
    keyboard=[
        [KeyboardButton('Голосование')],
        [KeyboardButton('Моя команда')],
        [KeyboardButton('Статистика')]
    ]
)

sport_types_ikb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton('ФУТБОЛ', callback_data='voting_soccer')],
        [InlineKeyboardButton('ХОККЕЙ', callback_data='voting_hockey')],
        [InlineKeyboardButton('БАСКЕТБОЛ', callback_data='voting_basketball')]
    ]
)