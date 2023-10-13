from aiogram import types
from aiogram.dispatcher import FSMContext
from database import (Database,
                      PROMPT_VIEW_TEAMS,
                      PROMPT_VIEW_NICKNAMES,
                      get_prompt_create_team,
                      get_prompts_leave_team,
                      get_prompt_view_teammates,
                      get_prompt_view_chat_id_by_nick,
                      get_prompt_view_user_team,
                      get_prompts_add_teammate,
                      get_prompt_view_team_size,
                      get_prompts_delete_team)
from .config import _ProfileStatesGroup
from ..bot_config import dp, bot
from ..keyboards import (confirm_leave_ikb,
                         confirm_delete_team_ikb,
                         get_teammate_ikb,
                         get_teammates_ikb)





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




@dp.callback_query_handler(lambda callback: callback.data.startswith('view_teammate_'))
async def view_teammate(callback: types.CallbackQuery) -> None:
    teammate_chat_id = callback.data.replace('view_teammate_', '')
    print(teammate_chat_id)

    await callback.message.edit_text(
        text=f'<a href="tg://user?id={teammate_chat_id}">Участник</a>',
        parse_mode='HTML'
    )
    await callback.message.edit_reply_markup(
        get_teammate_ikb(teammate_chat_id)
    )




@dp.callback_query_handler(lambda callback: callback.data.startswith('delete_teammate_'))
async def delete_teammate(callback: types.CallbackQuery) -> None:
    user_chat_id = callback.data.replace('delete_teammate_', '')
    
    db = Database()
    team_name = db.get_data_list(
        get_prompt_view_user_team(user_chat_id)
    )[0]['team_name']

    db.action(
        *get_prompts_leave_team(user_chat_id, team_name)
    )
    
    await callback.message.delete()
    await callback.message.answer('Участник удален')




@dp.callback_query_handler(lambda callback: callback.data.startswith('back_to_teammates_'))
async def back_to_teammates(callback: types.CallbackQuery) -> None:
    team_name = callback.data.replace('back_to_teammates_', '')
    await callback.message.edit_text(f'{team_name}\nСписок команды:')
    await callback.message.edit_reply_markup(
        get_teammates_ikb(
            user_chat_id=str(callback.message.chat.id), team_name=team_name
        )
    )




@dp.callback_query_handler(lambda callback: callback.data.startswith('add_teammate_'))
async def add_teammate(callback: types.CallbackQuery) -> None:
    team_name = callback.data.replace('add_teammate_', '')
    db = Database()
    team_size = db.get_data_list(
        get_prompt_view_team_size(team_name)
    )[0]['teammates']

    if team_size >= 10:
        await callback.message.answer(
            'Исчерпан лимит участников\nMAX 10 человек'
        )
        return
    
    await callback.message.answer(
        'Введите nickname человека, которого хотите добавить\n' \
        'Данный ник вводится при нажатии команды /start в этом боте'
    )
    await _ProfileStatesGroup.get_nickname_for_team.set()


@dp.message_handler(state=_ProfileStatesGroup.get_nickname_for_team)
async def get_team_name(message: types.Message, state=FSMContext) -> None:
    input_nickname = message.text

    db = Database()
    nicknames = [i['nickname'] for i in db.get_data_list(PROMPT_VIEW_NICKNAMES)]

    if input_nickname not in nicknames:
        await message.answer('Человек с таким именем не найден')
        await state.finish()
        return
    
    user_chat_id = db.get_data_list(
        get_prompt_view_chat_id_by_nick(input_nickname)
    )[0]['chat_id']

    is_user_in_team = db.get_data_list(
        get_prompt_view_user_team(user_chat_id)
    )[0]['team_name']

    if is_user_in_team:
        await message.answer(
            'Данного пользователя нельзя добавить, поскольку он уже состоит в другой команде'
        )
        await state.finish()
        return
    
    captain_chat_id = str(message.chat.id)
    team_name = db.get_data_list(
        get_prompt_view_user_team(captain_chat_id)
    )[0]['team_name']
    db.action(
        *get_prompts_add_teammate(user_chat_id, team_name)
    )

    await state.finish()
    await bot.send_message(user_chat_id, f'Вы были добавлены в команду {team_name}')
    await message.answer(f'Пользователь {input_nickname} добавлен')





@dp.callback_query_handler(lambda callback: callback.data == 'leave_team')
async def leave_team(callback: types.CallbackQuery) -> None:
    await callback.message.edit_text(
        text='Вы точно хотите выйти из команды?\nДобавить вас обратно может только администратор'
    )
    await callback.message.edit_reply_markup(confirm_leave_ikb)


@dp.callback_query_handler(lambda callback: callback.data == 'confirm_leave')
async def confirm_leave(callback: types.CallbackQuery) -> None:
    user_chat_id = str(callback.message.chat.id)

    db = Database()
    team_name = db.get_data_list(
        get_prompt_view_user_team(user_chat_id)
    )[0]['team_name']

    db.action(
        *get_prompts_leave_team(user_chat_id, team_name)
    )

    await callback.message.delete()
    await callback.message.answer('Вы покинули команду')




@dp.callback_query_handler(lambda callback: callback.data == 'delete_team')
async def delete_team(callback: types.CallbackQuery) -> None:
    await callback.message.edit_text('Вы уверены, что хотите удалить команду?')
    await callback.message.edit_reply_markup(confirm_delete_team_ikb)


@dp.callback_query_handler(lambda callback: callback.data == 'confirm_delete_team')
async def confirm_delete_team(callback: types.CallbackQuery) -> None:
    user_chat_id = str(callback.message.chat.id)

    db = Database()
    team_name = db.get_data_list(
        get_prompt_view_user_team(user_chat_id)
    )[0]['team_name']
    db.action(*get_prompts_delete_team(team_name))
    
    teammates_no_captain = db.get_data_list(
        get_prompt_view_teammates(team_name, user_chat_id)
    )

    for user in teammates_no_captain:
        await bot.send_message(
            chat_id=user['chat_id'],
            text='Ваша команда была удалена'
        )
    await callback.message.delete()
    await callback.message.answer(f'Команда {team_name} удалена')




@dp.callback_query_handler(lambda callback: callback.data == 'not_confirm')
async def not_confirm(callback: types.CallbackQuery) -> None:
    await callback.message.delete()