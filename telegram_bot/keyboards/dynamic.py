from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton



def get_question_ikb(quantity: int,
                     current_question_index: int,
                     coeffs: list[str],
                     answer: int = None) -> InlineKeyboardMarkup:
    # keyboard for the one question

    if not answer: pass
    elif answer == 1: team_1 = f"👉{team_1}👈"
    elif answer == 2: team_2 = f"👉{team_2}👈"
    else: draw = f"👉{draw}👈"

    if len(coeffs) == 3:
        inline_keyboard = [
            [
                InlineKeyboardButton(team_1, callback_data='first_team'),
                InlineKeyboardButton(draw, callback_data='draw'),
                InlineKeyboardButton(team_2, callback_data='second_team')
            ]
        ]
    else:
        inline_keyboard = [
            [
                InlineKeyboardButton(team_1, callback_data='first_team'),
                InlineKeyboardButton(team_2, callback_data='second_team')
            ]
        ]
    inline_keyboard.append([
        InlineKeyboardButton('<', callback_data='previous_question'),
        InlineKeyboardButton(f'{current_question_index + 1}/{quantity}', callback_data='0'),
        InlineKeyboardButton('>', callback_data='next_question')
    ])
    inline_keyboard.append(
        [InlineKeyboardButton('Назад', callback_data='back_to_sport_type')]
    )

    ikb = InlineKeyboardMarkup(inline_keyboard=inline_keyboard)
    return ikb