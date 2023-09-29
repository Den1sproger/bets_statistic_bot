from aiogram import types
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from database import (Database,
                      PROMPT_VIEW_TEAMS,
                      get_prompt_create_team,
                      get_prompt_leave_team)
from ..bot_config import dp
from ..keyboards import confirm_leave_ikb



class _ProfileStatesGroup(StatesGroup):
    get_team_name = State()


@dp.callback_query_handler(lambda callback: callback.data == 'create_team')
async def create_team(callback: types.CallbackQuery) -> None:
    await callback.message.delete()
    await callback.message.answer('Введите название команды')
    await _ProfileStatesGroup.get_team_name.set()


@dp.message_handler(state=_ProfileStatesGroup.get_team_name)
async def get_team_name(message: types.Message,
                        state: FSMContext) -> None:
    team_name = message.text
    user_chat_id = str(message.chat.id)

    db = Database()
    teams = [i['team_name'] for i in db.get_data_list(PROMPT_VIEW_TEAMS)]

    if team_name in teams:
        await message.answer('Это название уже занято, введите другое')
        return
    
    db.action(
        *get_prompt_create_team(team_name, user_chat_id)
    )
    await state.finish()
    await message.answer(
        text='Ваша команда успешно создана\nДля управления жмите кнопку "Моя команда"'
    )



@dp.callback_query_handler(lambda callback: callback.data == 'leave_team')
async def leave_team(callback: types.CallbackQuery) -> None:
    await callback.message.edit_text(
        text='Вы точно хотите выйти из команды?\nДобавить вас обратно сможет только администратор'
    )
    await callback.message.edit_reply_markup(confirm_leave_ikb)


@dp.callback_query_handler(lambda callback: callback.data == 'confirm_leave')
async def confirm_leave(callback: types.CallbackQuery) -> None:
    user_chat_id = str(callback.message.chat.id)

    await callback.message.delete()
    db = Database()
    db.action(get_prompt_leave_team(user_chat_id))
    
    await callback.message.answer('Вы покинули команду')



    
