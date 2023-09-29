from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from database import Database, get_prompt_view_votes



def get_question_ikb(quantity: int,
                     current_question_index: int,
                     coeffs: int,
                     answer: int = None,
                     game_key: str = None) -> InlineKeyboardMarkup:
    # keyboard for the one question
    if not answer:
        team_1 = 'П1'
        team_2 = 'П2'
        draw = 'X'
    else:
        db = Database()
        votes_data = db.get_data_list(get_prompt_view_votes(game_key))

        poole_first = votes_data['poole_first']
        poole_second = votes_data['poole_second']
        poole_draw = votes_data['poole_draw']

        if not poole_draw: poole_draw = 0

        all_votes = poole_first + poole_second + poole_draw
        
        part_first = int(round(100 * (poole_first/all_votes), 0))
        part_second = int(round(100 * (poole_second/all_votes), 0))
        part_draw = int(round(100 * (poole_draw/all_votes), 0))

        team_1 = f"{part_first}% - {poole_first} голосов"
        team_2 = f"{part_second}% - {poole_second} голосов"
        draw = f"{part_draw}% - {poole_draw} голосов"

        if answer == 1: team_1 = f"👉{team_1}👈"
        elif answer == 2: team_2 = f"👉{team_2}👈"
        else: draw = f"👉{draw}👈"

    if coeffs == 3:
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
        [InlineKeyboardButton('Назад', callback_data='back_to_sport_types')]
    )

    ikb = InlineKeyboardMarkup(inline_keyboard=inline_keyboard)
    return ikb