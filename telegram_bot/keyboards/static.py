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

team_create_ikb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton('Создать команду', callback_data='create_team')]
    ]
)

confirm_leave_ikb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton('Подтвердить', callback_data='confirm_leave')]
    ]
)