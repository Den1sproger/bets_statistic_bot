from aiogram import types
from aiogram.dispatcher.filters import Command, Text
from aiogram.dispatcher import FSMContext
from database import (Database,
                      get_prompt_view_user_stat,
                      get_prompt_view_user_team,
                      get_prompt_view_team_stat,
                      get_prompt_view_nickname_by_id,
                      get_prompt_update_nickname,
                      PROMPT_VIEW_POOLE_STAT,
                      PROMPT_VIEW_NICKNAMES)
from googlesheets import Stat_mass
from .config import _ProfileStatesGroup
from ..assets import VOTING_PHOTO_PATH
from ..bot_config import dp
from ..keyboards import (sport_types_ikb,
                         team_create_ikb,
                         get_teammates_ikb)



HELP_TEXT = """
/start - запустить бота
/help - помощь
/voting - голосование
/statistics - статистика
/myteam - моя команда
/nickname - обновить ник
"""


@dp.message_handler(Command('help'))
async def help(message: types.Message) -> None:
    await message.answer(HELP_TEXT)




@dp.message_handler(Text(equals='Голосование'))
@dp.message_handler(Command('voting'))
async def voting(message: types.Message) -> None:
    with open(VOTING_PHOTO_PATH, 'rb') as file:
        await message.answer_photo(photo=types.InputFile(file),
                                   caption='Выберите вид спорта',
                                   reply_markup=sport_types_ikb)



@dp.message_handler(Text(equals='Моя команда'))
@dp.message_handler(Command('myteam'))
async def my_team(message: types.Message) -> None:
    user_chat_id = str(message.chat.id)

    db = Database()
    user_team = db.get_data_list(
        get_prompt_view_user_team(user_chat_id)
    )[0]['team_name']

    if user_team:
        await message.answer(
            text=f'{user_team}\nСписок команды:',
            reply_markup=get_teammates_ikb(
                user_chat_id=user_chat_id, team_name=user_team
            )
        )
        return
    
    await message.answer(
        text='Вы не состоите в команде, можете создать команду и вы будете капитаном команды',
        reply_markup=team_create_ikb
    )



@dp.message_handler(Text(equals='Статистика'))
@dp.message_handler(Command('statistics'))
async def statistics(message: types.Message) -> None:
    user_chat_id = str(message.chat.id)
    db = Database()

    # user statistics
    user_stat = db.get_data_list(
        get_prompt_view_user_stat(user_chat_id)
    )[0]
    user_roi = user_stat['roi']
    if user_roi > 0:
        user_roi = f'+{user_roi}'

    # team statistics
    user_team = db.get_data_list(
        get_prompt_view_user_team(user_chat_id)
    )[0]['team_name']
    if user_team:
        team_stat = db.get_data_list(
            get_prompt_view_team_stat(user_team)
        )[0]
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
    poole_stat = db.get_data_list(PROMPT_VIEW_POOLE_STAT)[0]
    poole_roi = poole_stat['roi']
    if poole_roi > 0:
        poole_roi = f'+{poole_roi}'

    # message
    statistics_text = "<b>СТАТИСТИКА</b>\n" \
        f"Стат мой:✅{user_stat['positive_bets']}\t❌{user_stat['negative_bets']}\tROI {user_roi}\n" \
        f"Стат команды:✅{team_positive}\t❌{team_negative}\tROI {team_roi}\n" \
        f"Стат пула:✅{poole_stat['positive_bets']}\t❌{poole_stat['negative_bets']}\tROI {poole_roi}\n"
    
    await message.answer(statistics_text, parse_mode='HTML')




@dp.message_handler(Command('nickname'))
async def change_nick(message: types.Message) -> None:
    await _ProfileStatesGroup.get_new_nickname.set()
    await message.answer(
        '💬 Введите Ник, который будет отображаться в команде'
    )



@dp.message_handler(state=_ProfileStatesGroup.get_new_nickname)
async def get_nickname(message: types.Message, state: FSMContext) -> None:
    nickname = message.text
    user_chat_id = str(message.chat.id)

    db = Database()
    nicknames = [i['nickname'] for i in db.get_data_list(PROMPT_VIEW_NICKNAMES)]

    if nickname in nicknames:
        await message.answer(
            '❌❌Такой псевдоним уже занят'
        )
        await state.finish()
        return
    
    await state.finish()
    
    old_nick = db.get_data_list(
        get_prompt_view_nickname_by_id(user_chat_id)
    )[0]['nickname']
    
    gs_table = Stat_mass()           # update the nickname in users table
    gs_table.update_nickname(new_nick=nickname, old_nick=old_nick)

    db.action(
        get_prompt_update_nickname(
            chat_id=user_chat_id, new_nick=nickname
        )
    )

    await message.answer("✅ Ник принят")