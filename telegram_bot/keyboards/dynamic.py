from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from database import (Database,
                      get_prompt_view_votes,
                      get_prompt_view_captain,
                      get_prompt_view_nickname_by_id,
                      get_prompt_view_teammates,
                      get_prompt_view_team_votes,
                      get_prompt_view_user_team)



def get_question_ikb(quantity: int,
                     current_question_index: int,
                     coeffs: int,
                     team_name: str = None,
                     answer: int = None,
                     game_key: str = None) -> InlineKeyboardMarkup:
    # keyboard for the one question
    if answer:
        db = Database()
        votes_data = db.get_data_list(get_prompt_view_votes(game_key))[0]

        poole_first = votes_data['poole_first']
        poole_second = votes_data['poole_second']
        poole_draw = votes_data['poole_draw']

        if not poole_draw: poole_draw = 0

        all_votes = poole_first + poole_second + poole_draw
        
        part_first = int(round(100 * (poole_first/all_votes), 0))
        part_second = int(round(100 * (poole_second/all_votes), 0))
        part_draw = int(round(100 * (poole_draw/all_votes), 0))

        team_1 = f"{part_first}% - {poole_first} чел."
        team_2 = f"{part_second}% - {poole_second} чел."
        draw = f"{part_draw}% - {poole_draw} чел."

        if answer == 1: team_1 = f"👉{team_1}👈"
        elif answer == 2: team_2 = f"👉{team_2}👈"
        else: draw = f"👉{draw}👈"

    else:
        team_1 = 'П1'
        team_2 = 'П2'
        draw = 'X'

    inline_keyboard = []

    if team_name:
        db = Database()
        voted_teammates = db.get_data_list(
            get_prompt_view_team_votes(team_name)
        )

        msg_text = ''

        if len(voted_teammates) == 0:
            msg_text = '-'
        else:
            outcomes = [['П1', 0], ['П2', 0], ['Х', 0]]

            for teammate in voted_teammates:
                outcomes[teammate['answer'] - 1][1] += 1
            
            votes = (outcomes[0][1], outcomes[1][1], outcomes[2][1])
            team_select_votes = max(votes)

            team_outcome = ''
            for item in outcomes:
                if item[1] == team_select_votes:
                    team_outcome = item[0]
                    break
                
            msg_text = f'{team_outcome} - {round(team_select_votes / sum(votes) * 100, 0)}%'

        inline_keyboard.append([
            InlineKeyboardButton(f'Выбор команды {team_name}: {msg_text}', callback_data='0')
        ])

    if coeffs == 3:
        inline_keyboard.append([
            InlineKeyboardButton(team_1, callback_data='first_team'),
            InlineKeyboardButton(draw, callback_data='draw'),
            InlineKeyboardButton(team_2, callback_data='second_team')
        ])
    else:
        inline_keyboard.append([
            InlineKeyboardButton(team_1, callback_data='first_team'),
            InlineKeyboardButton(team_2, callback_data='second_team')
        ])

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


def get_teammates_ikb(team_name: str,
                      user_chat_id: str) -> InlineKeyboardMarkup:
    db = Database()

    captain_chat_id = db.get_data_list(
        get_prompt_view_captain(team_name)
    )[0]['captain_chat_id']
    captain_nick =  db.get_data_list(
        get_prompt_view_nickname_by_id(captain_chat_id)
    )[0]['nickname']
    
    inline_keyboard = []

    if captain_chat_id != user_chat_id:
        callback_data = ''
    else:
        callback_data = f'view_teammate'

    inline_keyboard.append([
        InlineKeyboardButton(
            text=f'{captain_nick} - капитан', callback_data=f"{callback_data}_{captain_chat_id}"
        )
    ])

    teammates_no_captain = db.get_data_list(
        get_prompt_view_teammates(team_name, captain_chat_id)
    )

    for user in teammates_no_captain:
        inline_keyboard.append([
            InlineKeyboardButton(text=user['nickname'], callback_data=f"{callback_data}_{user['chat_id']}")
        ])

    if captain_chat_id != user_chat_id:
        inline_keyboard.append(
            [InlineKeyboardButton('Выйти из команды', callback_data='leave_team')]
        )
    else:
        inline_keyboard += [
            [InlineKeyboardButton('Добавить участника', callback_data=f'add_teammate_{team_name}')],
            [InlineKeyboardButton('Удалить команду', callback_data='delete_team')],
        ]
    
    inline_keyboard.append(
        [InlineKeyboardButton('ГЛАВНОЕ МЕНЮ', callback_data='main_menu')]
    )
    ikb = InlineKeyboardMarkup(inline_keyboard=inline_keyboard)
    return ikb


def get_teammate_ikb(teammate_chat_id: str) -> InlineKeyboardMarkup:
    inline_keyboard = []

    db = Database()
    team_name = db.get_data_list(
        get_prompt_view_user_team(teammate_chat_id)
    )[0]['team_name']

    captain_chat_id = db.get_data_list(
        get_prompt_view_captain(team_name)
    )[0]['captain_chat_id']

    if teammate_chat_id != captain_chat_id:
        inline_keyboard.append(
            [InlineKeyboardButton('Удалить участника', callback_data=f"delete_teammate_{teammate_chat_id}")]
        )

    inline_keyboard.append(
        [InlineKeyboardButton('Вернуться к участникам', callback_data=f"back_to_teammates_{team_name}")]
    )

    return InlineKeyboardMarkup(inline_keyboard=inline_keyboard)



def get_invitation_to_team_ikb(team_name: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton('Принять', callback_data=f'accept_invitation_{team_name}')],
            [InlineKeyboardButton('Отклонить', callback_data=f'decline_invitation_{team_name}')]
        ]
    )