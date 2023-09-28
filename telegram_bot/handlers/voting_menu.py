from aiogram import types
from ..bot_config import dp
from ..keyboards import get_question_ikb
from database import (Database,
                      get_prompt_view_games,
                      PROMPT_VIEW_CURRENT_CHAT_iDS,
                      get_prompt_add_current_info,
                      get_prompt_update_current_index,
                      get_prompt_view_current_info,
                      get_prompt_view_answer,
                      get_prompt_update_answer,
                      get_prompt_add_answer)



sport_symbols = {
    'ФУТБОЛ': ' ⚽️⚽️⚽️',
    'ХОККЕЙ': '🏒🏒🏒',
    'БАСКЕТБОЛ': '🏀🏀🏀'
}

questions = {
    'SOCCER': [],
    'HOCKEY': [],
    'BASKETBALL': []
}


def get_current_data(db: Database,
                     chat_id: str,
                     sport_type: str) -> dict:
    data = db.get_data_list(
        get_prompt_view_current_info(chat_id)
    )[0]

    current_index = data.get('current_index')

    games_number = len(questions[sport_type])
    if current_index < 0:
        current_index = games_number - 1
        db.action(get_prompt_update_current_index(chat_id, current_index))
    elif current_index >= games_number:
        current_index = 0
        db.action(get_prompt_update_current_index(chat_id, current_index))

    current_game = questions[sport_type][current_index]

    return current_index, current_game



def get_update_msg(game: dict,
                   index: int,
                   sport_type: str,
                   answer: int = None) -> types.InlineKeyboardMarkup and str:    
    coeff_1 = game['first_coeff']
    coeff_2 = game['second_coeff']
    draw_coeff = game['draw_coeff']
    coeffs_txt = ''
    if draw_coeff == None:
        coeffs = [coeff_1, coeff_2]
        coeffs_txt = f'П1-{coeff_1}  П2-{coeff_2}'
    else:
        coeffs = [coeff_1, coeff_2, draw_coeff]
        coeffs_txt = f'П1-{coeff_1}  X-{draw_coeff}  П2-{coeff_2}'

    msg_text = f'{game["sport"].upper()}{sport_symbols[game["sport"].upper()]}\n\n' \
        f'МАТЧ: {game["first_team"]} - {game["second_team"]}\n' \
        f'НАЧАЛО: {game["begin_time"]}\n' \
        f'КОЭФФИЦИЕНТЫ: {coeffs_txt}\n\n' \
        f'ОБЗОР МАТЧА:\n{game["url"]}'
    
    return get_question_ikb(
        quantity=len(questions[sport_type]),
        current_question_index=index,
        coeffs=coeffs, answer=answer,
        game_key=game['game_key']
    ), msg_text



# update data of question for the message and edit the message
async def update_questions_data(callback: types.CallbackQuery,
                                sport_type: str) -> None:
    user_chat_id = str(callback.message.chat.id)
    db = Database()
    current_index, current_game = get_current_data(db, user_chat_id, sport_type)

    answer = db.get_data_list(
        get_prompt_view_answer(
            chat_id=user_chat_id,
            game_key=current_game['game_key']
        )
    )
    if answer:
        answer = answer[0]['answer']
    else:
        answer = None
        
    reply_markup, msg_text = get_update_msg(
        game=current_game, answer=answer,
        index=current_index, type_=sport_type
    )
    
    await callback.message.edit_text(msg_text)
    await callback.message.edit_reply_markup(reply_markup=reply_markup)

    

async def answer(answer: int,
                 callback: types.CallbackQuery) -> None:
    user_chat_id = str(callback.message.chat.id)
    db = Database()

    data, current_game = get_current_data(db, user_chat_id)

    game_key = current_game['game_key']
    index = data['index']
    tournament = data['tournament']
    type_= data['type']

    reply_markup, _ = get_update_msg(
        game=current_game, answer=answer, index=index,
        tournament=tournament, type_= type_
    )

    old_answer = db.get_data_list(
        get_prompt_view_answer(
            chat_id=user_chat_id,
            tournament=tournament, game_key=game_key
        )
    )
    prompt = ''
    if old_answer:
        if old_answer[0]['answer'] == answer:
            return
        prompt = get_prompt_update_answer(
            chat_id=user_chat_id,
            game_key=game_key, new_answer=answer
        )
    else:
        prompt = get_prompt_add_answer(
            chat_id=user_chat_id,
            game_key=game_key, answer=answer
        )
    db.action(prompt)
    
    await callback.message.edit_reply_markup(reply_markup=reply_markup)



# selected sport type for voting
@dp.callback_query_handler(lambda callback: callback.data.startswith('voting_'))
async def get_voting_board(callback: types.CallbackQuery) -> None:
    sport_type = callback.data.replace('voting_', '')
    
    db = Database()
    games = db.get_data_list(get_prompt_view_games(sport_type))

    global questions

    if games:
        if games != questions[sport_type]:
            questions[sport_type] = games

        user_chat_id = str(callback.message.chat.id)
        chat_ids = [i['chat_id'] for i in db.get_data_list(PROMPT_VIEW_CURRENT_CHAT_iDS)]
        if user_chat_id not in chat_ids:
            db.action(
                get_prompt_add_current_info(user_chat_id)
            )
        else:
            db.action(
                get_prompt_update_current_index(user_chat_id)
            )
        await update_questions_data(callback, sport_type)

    else:
        await callback.answer('В данный момент голосование недоступно')