from aiogram import types
from ..bot_config import dp
from ..keyboards import sport_types_ikb, get_question_ikb
from database import (Database,
                      get_prompt_view_games,
                      PROMPT_VIEW_CURRENT_CHAT_iDS,
                      get_prompt_add_current_info,
                      get_prompt_update_current_index,
                      get_prompt_view_current_info,
                      get_prompt_view_answer,
                      get_prompt_update_answer,
                      get_prompt_add_answer,
                      get_prompt_increase_current_index,
                      get_prompt_decrease_current_index,
                      get_prompt_delete_current_info)



sport_symbols = {
    'ФУТБОЛ': ' ⚽️⚽️⚽️',
    'ХОККЕЙ': '🏒🏒🏒',
    'БАСКЕТБОЛ': '🏀🏀🏀'
}

questions = {
    'Футбол': [],
    'Хоккей': [],
    'Баскетбол': []
}


def get_current_data(db: Database,
                     chat_id: str) -> dict:
    data = db.get_data_list(
        get_prompt_view_current_info(chat_id)
    )[0]

    current_index = data.get('current_index')
    sport_type = data.get('sport_type')

    games_number = len(questions[sport_type])
    if current_index < 0:
        current_index = games_number - 1
        db.action(get_prompt_update_current_index(chat_id, current_index))
    elif current_index >= games_number:
        current_index = 0
        db.action(get_prompt_update_current_index(chat_id, current_index))

    current_game = questions[sport_type][current_index]

    return current_index, sport_type, current_game



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
async def update_questions_data(callback: types.CallbackQuery) -> None:
    user_chat_id = str(callback.message.chat.id)
    db = Database()
    current_index, sport_type, current_game = get_current_data(db, user_chat_id)

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
        index=current_index, sport_type=sport_type
    )
    
    await callback.message.edit_text(msg_text)
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
                get_prompt_add_current_info(user_chat_id, sport_type)
            )
        else:
            db.action(
                get_prompt_update_current_index(user_chat_id)
            )
        await update_questions_data(callback)

    else:
        await callback.answer('В данный момент голосование недоступно')


    
async def answer(answer: int,
                 callback: types.CallbackQuery) -> None:
    user_chat_id = str(callback.message.chat.id)
    db = Database()

    data, current_game = get_current_data(db, user_chat_id)

    game_key = current_game['game_key']
    index = data['index']
    type_= data['type']

    reply_markup, _ = get_update_msg(
        game=current_game, answer=answer, index=index, type_= type_
    )

    old_answer = db.get_data_list(
        get_prompt_view_answer(
            chat_id=user_chat_id, game_key=game_key
        )
    )
    prompts = []
    if old_answer:
        if old_answer[0]['answer'] == answer:
            return
        prompts.append(
            get_prompt_update_answer(
                chat_id=user_chat_id,
                game_key=game_key, new_answer=answer
            )
        )
    else:
        prompts.append(
            get_prompt_add_answer(
                chat_id=user_chat_id,
                game_key=game_key, answer=answer
            )
        )
        
    db.action(*prompts)
    
    await callback.message.edit_reply_markup(reply_markup=reply_markup)



# next question
@dp.callback_query_handler(lambda callback: callback.data == 'next_question')
async def next_question(callback: types.CallbackQuery) -> None:
    user_chat_id = str(callback.message.chat.id)
    db = Database()
    db.action(get_prompt_increase_current_index(user_chat_id))

    await update_questions_data(callback)


# previous question
@dp.callback_query_handler(lambda callback: callback.data == 'previous_question')
async def previous_question(callback: types.CallbackQuery) -> None:
    user_chat_id = str(callback.message.chat.id)
    db = Database()
    db.action(get_prompt_decrease_current_index(user_chat_id))

    await update_questions_data(callback)



@dp.callback_query_handler(lambda callback: callback.data == 'first_team')
async def first_team(callback: types.CallbackQuery) -> None:
    await answer(answer=1, callback=callback)


@dp.callback_query_handler(lambda callback: callback.data == 'second_team')
async def second_team(callback: types.CallbackQuery) -> None:
    await answer(answer=2, callback=callback)


@dp.callback_query_handler(lambda callback: callback.data == 'draw')
async def draw(callback: types.CallbackQuery) -> None:
    await answer(answer=3, callback=callback)


# come back to the menu of sport_types
@dp.callback_query_handler(lambda callback: callback.data == 'back_to_sport_types')
async def back_to_tourns(callback: types.CallbackQuery) -> None:
    user_chat_id = str(callback.message.chat.id)
    db = Database()

    db.action(
        get_prompt_delete_current_info(user_chat_id)
    )

    await callback.message.edit_text('Выберите вид спорта')
    await callback.message.edit_reply_markup(reply_markup=sport_types_ikb)