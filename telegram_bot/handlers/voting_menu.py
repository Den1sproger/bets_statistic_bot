from datetime import datetime
from aiogram import types
from ..bot_config import dp
from ..keyboards import sport_types_ikb, get_question_ikb
from ..assets import VOTING_PHOTO_PATH
from googlesheets import Games
from database import (Database,
                      get_prompt_view_games,
                      PROMPT_VIEW_CURRENT_CHAT_iDS,
                      get_prompt_add_current_info,
                      get_prompt_update_current_index,
                      get_prompt_view_current_info,
                      get_prompt_view_answer,
                      get_prompt_add_answer,
                      get_prompt_increase_current_index,
                      get_prompt_decrease_current_index,
                      get_prompt_delete_current_info,
                      get_prompt_update_current_info,
                      get_prompt_update_vote,
                      get_prompt_view_user_team,
                      get_prompt_update_game_status)



sport_symbols = {
    'ФУТБОЛ': '⚽️⚽️⚽️',
    'ХОККЕЙ': '🏒🏒🏒',
    'БАСКЕТБОЛ': '🏀🏀🏀'
}

questions = {
    'Футбол': [],
    'Хоккей': [],
    'Баскетбол': []
}


def get_current_data(db: Database,
                     chat_id: str) -> str | int | dict:
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
                   db: Database,
                   user_chat_id: str | int, 
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
    
    user_team = db.get_data_list(
        get_prompt_view_user_team(user_chat_id)
    )[0]['team_name']

    return get_question_ikb(
        quantity=len(questions[sport_type]),
        current_question_index=index,
        team_name=user_team,
        coeffs=len(coeffs), answer=answer,
        game_key=game['game_key']
    ), msg_text



# update data of question for the message and edit the message
async def update_questions_data(callback: types.CallbackQuery,
                                edit: bool = True) -> None:
    user_chat_id = str(callback.message.chat.id)
    db = Database()
    current_index, sport_type, current_game = get_current_data(db, user_chat_id)

    answer = db.get_data_list(
        get_prompt_view_answer(
            chat_id=user_chat_id,
            game_key=current_game['game_key']
        )
    )
    if answer: answer = answer[0]['answer']
    else: answer = None

    reply_markup, msg_text = get_update_msg(
        game=current_game, answer=answer,
        db=db, user_chat_id=user_chat_id,
        index=current_index, sport_type=sport_type
    )
    
    if edit:
        await callback.message.edit_text(msg_text)
        await callback.message.edit_reply_markup(reply_markup=reply_markup)
    else:
        await callback.message.delete()
        await callback.message.answer(msg_text, reply_markup=reply_markup)



# click on sport type button for voting
@dp.callback_query_handler(lambda callback: callback.data.startswith('voting_'))
async def get_voting_board(callback: types.CallbackQuery) -> None:
    sport_type = callback.data.replace('voting_', '')

    db = Database()
    games = db.get_data_list(get_prompt_view_games(sport_type))

    global questions

    if not games:
        await callback.answer('В данный момент голосование недоступно')
        return

    # check games on the begin
    prompts = []
    games_for_del = []
    time_now = datetime.now()

    for game in games:
        game_begin_time = datetime.strptime(game['begin_time'], '%Y-%m-%d %H:%M')
        if time_now >= game_begin_time:
            prompts.append(
                get_prompt_update_game_status(game['game_key'], status=2)
            )
            games_for_del.append(game)

    if prompts: db.action(*prompts)            # update statuses in database
    for game in games_for_del: games.remove(game)       # delete started games from current list
    
    # if all games is already start
    if not games:
        await callback.answer('Голосование недоступно')
        return

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
            get_prompt_update_current_info(user_chat_id, sport_type)
        )
    await update_questions_data(callback, edit=False)


    
async def answer(answer: int,
                 callback: types.CallbackQuery) -> None:
    user_chat_id = str(callback.message.chat.id)
    db = Database()

    index, sport_type, current_game = get_current_data(db, user_chat_id)

    game_key = current_game['game_key']

    old_answer = db.get_data_list(
        get_prompt_view_answer(
            chat_id=user_chat_id, game_key=game_key
        )
    )

    if old_answer: return
    else:
        user_team = db.get_data_list(
            get_prompt_view_user_team(user_chat_id)
        )[0]['team_name']

        prompts = [
            get_prompt_update_vote(game_key, answer, action='+'),
            get_prompt_add_answer(
                chat_id=user_chat_id,
                game_key=game_key, answer=answer,
                team_name=user_team
            )
        ]
        
    db.action(*prompts)
    
    reply_markup, _ = get_update_msg(
        game=current_game, answer=answer,
        index=index, sport_type=sport_type,
        db=db, user_chat_id=user_chat_id
    )

    games_gs = Games()
    games_gs.update_votes(game_key)

    await callback.message.edit_reply_markup(reply_markup=reply_markup)



# click on arrow of next question
@dp.callback_query_handler(lambda callback: callback.data == 'next_question')
async def next_question(callback: types.CallbackQuery) -> None:
    user_chat_id = str(callback.message.chat.id)
    db = Database()
    db.action(get_prompt_increase_current_index(user_chat_id))

    await update_questions_data(callback)


# click on arrow of previous question
@dp.callback_query_handler(lambda callback: callback.data == 'previous_question')
async def previous_question(callback: types.CallbackQuery) -> None:
    user_chat_id = str(callback.message.chat.id)
    db = Database()
    db.action(get_prompt_decrease_current_index(user_chat_id))

    await update_questions_data(callback)



@dp.callback_query_handler(lambda callback: callback.data == 'first_team')         # click on the first team button
async def first_team(callback: types.CallbackQuery) -> None:
    await answer(answer=1, callback=callback)


@dp.callback_query_handler(lambda callback: callback.data == 'second_team')        # click on the second team button
async def second_team(callback: types.CallbackQuery) -> None:
    await answer(answer=2, callback=callback)


@dp.callback_query_handler(lambda callback: callback.data == 'draw')               # click on the draw button
async def draw(callback: types.CallbackQuery) -> None:
    await answer(answer=3, callback=callback)


# click the button of come back to the menu of sport_types
@dp.callback_query_handler(lambda callback: callback.data == 'back_to_sport_types')
async def back_to_tourns(callback: types.CallbackQuery) -> None:
    user_chat_id = str(callback.message.chat.id)
    db = Database()
    db.action(
        get_prompt_delete_current_info(user_chat_id)
    )

    await callback.message.delete()

    with open(VOTING_PHOTO_PATH, 'rb') as file:
        await callback.message.answer_photo(photo=types.InputFile(file),
                                            reply_markup=sport_types_ikb)