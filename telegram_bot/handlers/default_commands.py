import tabulate

from aiogram import types
from aiogram.dispatcher.filters import Command, Text
from aiogram.dispatcher import FSMContext
from database import (Database,
                      get_prompt_view_user_stat,
                      get_prompt_view_user_team,
                      get_prompt_view_team_stat,
                      get_prompt_update_nickname,
                      get_prompts_reset_user_stat,
                      PROMPT_VIEW_POOLE_STAT,
                      PROMPT_VIEW_NICKNAMES)
from googlesheets import Stat_mass, Stat_sport_types
from .config import _ProfileStatesGroup
from ..assets import VOTING_PHOTO_PATH, TEAM_PHOTO_PATH
from ..bot_config import dp
from ..keyboards import (sport_types_ikb,
                         team_create_ikb,
                         main_kb,
                         confirm_reset_stat_ikb,
                         get_teammates_ikb)



HELP_TEXT = """
/start - запустить бота
/help - помощь
/voting - голосование
/my_team - моя команда
/statistics - статистика
/nickname - обновить ник
/reset_my_stat - обнулить стат
"""


@dp.message_handler(Command('help'))
async def help(message: types.Message) -> None:
    await message.answer(HELP_TEXT, reply_markup=main_kb)




@dp.message_handler(Text(equals='Голосование'))
@dp.message_handler(Command('voting'))
async def show_voting(message: types.Message) -> None:
    with open(VOTING_PHOTO_PATH, 'rb') as file:
        await message.answer_photo(photo=types.InputFile(file),
                                   reply_markup=sport_types_ikb)
    await message.delete()




@dp.message_handler(Text(equals='Моя команда'))
@dp.message_handler(Command('my_team'))
async def show_my_team(message: types.Message) -> None:
    user_chat_id = str(message.chat.id)

    db = Database()
    user_team = db.get_data_list(
        get_prompt_view_user_team(user_chat_id)
    )[0]['team_name']

    if user_team:
        await message.answer(
            text='👥 Список участников команды',
            reply_markup=get_teammates_ikb(
                user_chat_id=user_chat_id, team_name=user_team
            )
        )
        return
    
    with open(TEAM_PHOTO_PATH, 'rb') as file:
        await message.answer_photo(
            photo=types.InputFile(file),
            reply_markup=team_create_ikb
        )




@dp.message_handler(Text(equals='Статистика'))
@dp.message_handler(Command('statistics'))
async def show_statistics(message: types.Message) -> None:
    user_chat_id = str(message.chat.id)
    db = Database()

    # user statistics
    user_stat = db.get_data_list(
        get_prompt_view_user_stat(user_chat_id)
    )[0]
    user_roi = round(user_stat['roi'], 3)
    user_profit = user_stat['coeff_sum'] - user_stat['positive_bets'] - user_stat['negative_bets']
    user_profit = round(user_profit, 2)

    if user_roi > 0:
        user_roi = f'+{user_roi}'
    if user_profit > 0:
        user_profit = f"+{user_profit}"

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
        team_profit = team_stat['coeff_sum'] - team_positive - team_negative

        if team_roi > 0:
            team_roi = f'+{team_roi}'
        if team_profit > 0:
            team_profit = f'+{team_profit}'
    else:
        team_positive = 0
        team_negative = 0
        team_roi = 0
        team_profit = 0

    # poole statistics
    poole_stat = db.get_data_list(PROMPT_VIEW_POOLE_STAT)[0]
    poole_roi = round(poole_stat['roi'], 3)
    poole_profit = poole_stat['coeff_sum'] - poole_stat['positive_bets'] - poole_stat['negative_bets']
    poole_profit = round(poole_profit, 2)

    if poole_roi > 0:
        poole_roi = f'+{poole_roi}'
    if poole_profit > 0:
        poole_profit = f'+{poole_profit}'
    # message

    data = [
        [
            'MY:',
            f"✅{user_stat['positive_bets']}",
            f"❌{user_stat['negative_bets']}",
            f"📈{user_roi}%", f"💰{user_profit}K"
        ],
        [
            'TEAM:',
            f"✅{team_positive}",
            f"❌{team_negative}",
            f"📈{round(float(team_roi), 3)}%",
            f"💰{round(float(team_profit), 2)}K"
        ],
        [
            'POOL:',
            f"✅{poole_stat['positive_bets']}",
            f"❌{poole_stat['negative_bets']}",
            f"📈{poole_roi}%",
            f"💰{poole_profit}K"
        ]
    ]
    table = tabulate.tabulate(data, tablefmt="plain")
    statistics_text = f"📊 <b>СТАТИСТИКА</b> 📊\n" \
        f"<pre>{table}</pre>\n\n" \
        "Все расчеты выполнены с учетом\nпостоянной ставки в 1000 ₽\n\n" \
        "Условные обозначения:\n" \
        "✅ - количество побед\n❌ - количество поражений\n📈 - процент выигрыша на одну ставку (ROI)\n💰 - чистая прибыль за все время"
    
    await message.answer(text=statistics_text,
                         parse_mode=types.ParseMode.HTML,
                         reply_markup=main_kb)




@dp.message_handler(Command('nickname'))
async def change_nick(message: types.Message) -> None:
    await _ProfileStatesGroup.get_new_nickname.set()
    await message.answer('📍 Введите новый Ник')



@dp.message_handler(state=_ProfileStatesGroup.get_new_nickname)
async def get_nickname(message: types.Message, state: FSMContext) -> None:
    nickname = message.text
    user_chat_id = str(message.chat.id)

    db = Database()
    nicknames = [i['nickname'] for i in db.get_data_list(PROMPT_VIEW_NICKNAMES)]

    if nickname in nicknames:
        await message.answer(
            '❌ Этот Ник уже занят\n📍 Введите новый Ник'
        )
        await state.finish()
        return
    
    await state.finish()
    
    gs_table = Stat_mass()           # update the nickname in users table
    gs_table.update_nickname(new_nick=nickname, chat_id=user_chat_id)

    db.action(
        get_prompt_update_nickname(
            chat_id=user_chat_id, new_nick=nickname
        )
    )

    await message.answer("🟢 Ник принят")




@dp.message_handler(Command('reset_my_stat'))
async def reset_user_stat(message: types.Message) -> None:
    await message.answer(
        text='Вы уверены что хотите обнулить свой стат?\nОтменить это действие будет невозможно',
        reply_markup=confirm_reset_stat_ikb
    )


@dp.callback_query_handler(lambda callback: callback.data == 'confirm_reset_stat')
async def confirm_reset_stat(callback: types.CallbackQuery) -> None:
    await callback.message.delete()

    user_chat_id = str(callback.message.chat.id)

    sm = Stat_mass()
    sm.reset_user_stat(user_chat_id)

    sst = Stat_sport_types()
    sst.reset_user_stat(user_chat_id)

    db = Database()
    db.action(*get_prompts_reset_user_stat(user_chat_id))

    await callback.message.answer('✅Ваш стат обнулен')
    

