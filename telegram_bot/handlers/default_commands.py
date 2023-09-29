from aiogram import types
from aiogram.dispatcher.filters import Command, Text
from database import (Database,
                      get_prompt_view_user_stat,
                      get_prompt_view_user_team,
                      get_prompt_view_team_stat,
                      PROMPT_VIEW_POOLE_STAT)
from ..bot_config import dp
from ..keyboards import sport_types_ikb



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


@dp.message_handler(Text(equals='Голосование'))
@dp.message_handler(Command('voting'))
async def voting(message: types.Message) -> None:
    await message.answer('Выберите вид спорта', reply_markup=sport_types_ikb)


@dp.message_handler(Text(equals='Моя команда'))
@dp.message_handler(Command('myteam'))
async def my_team(message: types.Message) -> None:
    user_chat_id = str(message.chat.id)

    # db = Database()
    # user_team = db.get_data_list(
    #     get_prompt_view_user_team(user_chat_id)
    # )[0]['team_name']
    # if user_team:
    #     teammates = db.get_data_list()
    


@dp.message_handler(Text(equals='Статистика'))
@dp.message_handler(Command('statistics'))
async def statistics(message: types.Message) -> None:
    user_chat_id = str(message.chat.id)
    db = Database()

    # user statistics
    user_stat = db.get_data_list(
        get_prompt_view_user_stat(user_chat_id)
    )
    user_roi = user_stat[0]['roi']
    if user_roi > 0:
        user_roi = f'+{user_roi}'

    # team statistics
    user_team = db.get_data_list(
        get_prompt_view_user_team(user_chat_id)
    )[0]['team_name']
    if user_team:
        team_stat = db.get_data_list(
            get_prompt_view_team_stat(user_team)
        )
        team_positive = team_stat['positive_bets']
        team_negative = team_stat['negative_bets']
        team_roi = team_stat['roi']
        if team_roi > 0:
            team_roi = f'+{team_roi}'
    else:
        team_positive = 0
        team_negative = 0
        team_roi = 0

    # poole statistics
    poole_stat = db.get_data_list(PROMPT_VIEW_POOLE_STAT)
    poole_roi = poole_stat[0]['roi']
    if poole_roi > 0:
        poole_roi = f'+{poole_roi}'

    # message
    statistics_text = "**СТАТИСТИКА**\n" \
        f"Стат мой:\t\t✅{user_stat['positive_bets']}\t❌{user_stat['negative_bets']}\tROI {user_roi}\n" \
        f"Стат команды:\t✅{team_positive}\t❌{team_negative}\tROI {team_roi}\n" \
        f"Стат пула:&nbsp;&nbsp;&nbsp;\t✅{poole_stat['positive_bets']}\t❌{poole_stat['negative_bets']}\tROI {poole_roi}\n"
    
    await message.answer(statistics_text, parse_mode='Markdown')