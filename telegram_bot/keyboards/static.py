from aiogram.types import (InlineKeyboardMarkup,
                           InlineKeyboardButton)


main_ikb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton('Голосование', callback_data='main_voting')],
        [InlineKeyboardButton('Моя команда', callback_data='main_my_team')],
        [InlineKeyboardButton('Статистика', callback_data='main_statistics')]
    ]
)

sport_types_ikb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton('ФУТБОЛ', callback_data='voting_Футбол')],
        [InlineKeyboardButton('ХОККЕЙ', callback_data='voting_Хоккей')],
        [InlineKeyboardButton('БАСКЕТБОЛ', callback_data='voting_Баскетбол')],
        [InlineKeyboardButton('ГЛАВНОЕ МЕНЮ', callback_data='main_menu')]
    ]
)

team_create_ikb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton('Создать команду', callback_data='create_team')],
        [InlineKeyboardButton('ГЛАВНОЕ МЕНЮ', callback_data='main_menu')]
    ]
)

confirm_leave_ikb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton('Подтвердить', callback_data='confirm_leave')],
        [InlineKeyboardButton('Отмена', callback_data='not_confirm')]
    ]
)

confirm_delete_team_ikb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton('Подтвердить', callback_data='confirm_delete_team')],
        [InlineKeyboardButton('Отмена', callback_data='not_confirm')]
    ]
)

back_to_main_menu_ikb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton('ГЛАВНОЕ МЕНЮ', callback_data='main_menu')]
    ]
)