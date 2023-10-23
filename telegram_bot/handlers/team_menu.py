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
                      get_prompts_delete_team,
                      get_prompt_view_captain,
                      get_prompt_view_nickname_by_id)
from ..assets import TEAM_PHOTO_PATH
from .config import _ProfileStatesGroup
from ..bot_config import dp, bot
from ..keyboards import (confirm_leave_ikb,
                         confirm_delete_team_ikb,
                         get_invitation_to_team_ikb,
                         get_teammate_ikb,
                         get_teammates_ikb)




@dp.callback_query_handler(lambda callback: callback.data == 'create_team')
async def create_team(callback: types.CallbackQuery) -> None:
    await callback.message.delete()
    with open(TEAM_PHOTO_PATH, 'rb') as file:
        await callback.message.answer_photo(
            photo=types.InputFile(file),
            caption='📍Введите название своей команды'
        )
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
        text='🟢 Ваша команда успешно создана\n\n' \
        '📣 ОСНОВНЫЕ ПОЛОЖЕНИЯ\n' \
        '♦️ команда может включать в себя до 10 участников\n' \
        '♦️ участник может состоять только в одной команде\n' \
        '♦️ итоговый выбор команды осуществляется по большему количеству голосов\n'
    )
    await message.answer(
        text='👥 Список участников команды:',
        reply_markup=get_teammates_ikb(
            user_chat_id=user_chat_id, team_name=team_name
        )
    )




@dp.callback_query_handler(lambda callback: callback.data.startswith('view_teammate_'))
async def view_teammate(callback: types.CallbackQuery) -> None:
    teammate_chat_id = callback.data.replace('view_teammate_', '')

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
    await bot.send_message(
        chat_id=user_chat_id,
        text=f"Вы были удалены из команды {team_name}"
    )



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
    
    await state.finish()
    
    captain_chat_id = str(message.chat.id)
    team_name = db.get_data_list(
        get_prompt_view_user_team(captain_chat_id)
    )[0]['team_name']
    db.action(
        *get_prompts_add_teammate(user_chat_id, team_name)
    )

    await state.finish()
    await bot.send_message(
        chat_id=user_chat_id,
        text=f'Вас хотят пригласить в команду {team_name}',
        reply_markup=get_invitation_to_team_ikb(team_name)
    )
    await message.answer(f'Пользователю {input_nickname} отправлено приглашение')


@dp.callback_query_handler(lambda callback: callback.data.startswith('accept_invitation_'))
async def accept_invitation(callback: types.CallbackQuery) -> None:
    team_name = callback.data.replace('accept_invitation_', '')
    user_chat_id = str(callback.message.chat.id)

    db = Database()
    db.action(
        *get_prompts_add_teammate(user_chat_id, team_name)
    )
    nickname = db.get_data_list(
        get_prompt_view_nickname_by_id(user_chat_id)
    )[0]['nickname']
    captain_chat_id = db.get_data_list(
        get_prompt_view_captain(team_name)
    )[0]['captain_chat_id']

    await bot.send_message(
        captain_chat_id,
        f'Пользователь {nickname} принял ваше приглашение в команду'
    )

    await callback.message.answer(
        text='🟢 Вы успешно добавлены \n\n' \
        '📣 ОСНОВНЫЕ ПОЛОЖЕНИЯ\n' \
        '♦️ команда может включать в себя до 10 участников\n' \
        '♦️ участник может состоять только в одной команде\n' \
        '♦️ итоговый выбор команды осуществляется по большему количеству голосов\n'
    )
    await callback.message.answer(
        text='👥 Список участников команды:',
        reply_markup=get_teammates_ikb(
            user_chat_id=user_chat_id, team_name=team_name
        )
    )


@dp.callback_query_handler(lambda callback: callback.data.startswith('decline_invitation_'))
async def decline_invitation(callback: types.CallbackQuery) -> None:
    team_name = callback.data.replace('decline_invitation_', '')
    user_chat_id = str(callback.message.chat.id)

    db = Database()
    nickname = db.get_data_list(
        get_prompt_view_nickname_by_id(user_chat_id)
    )[0]['nickname']
    captain_chat_id = db.get_data_list(
        get_prompt_view_captain(team_name)
    )[0]['captain_chat_id']

    await bot.send_message(
        captain_chat_id,
        f'Пользователь {nickname} отклонил ваше приглашение в команду'
    )




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

    captain_chat_id = db.get_data_list(
        get_prompt_view_captain(team_name)
    )[0]['captain_chat_id']

    nickname = db.get_data_list(
        get_prompt_view_nickname_by_id(user_chat_id)
    )[0]['nickname']

    db.action(
        *get_prompts_leave_team(user_chat_id, team_name)
    )

    await callback.message.delete()
    await callback.message.answer('Вы покинули команду')
    await bot.send_message(
        chat_id=captain_chat_id,
        text=f'{nickname} покинул команду'
    )




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