from aiogram import types
from aiogram.dispatcher.filters import Command
from aiogram.dispatcher import FSMContext
from aiogram.types.bot_command_scope import BotCommandScopeChat
from googlesheets import Stat_mass, Stat_sport_types
from database import (Database,
                      get_prompts_add_user,
                      get_prompt_update_nickname,
                      PROMPT_VIEW_ALL_CHAT_IDS,
                      PROMPT_VIEW_NICKNAMES)
from .config import _ProfileStatesGroup
from ..assets import START_PHOTO_PATH
from ..bot_config import dp, bot, default_commands
from ..keyboards import main_kb




@dp.message_handler(Command('start'))
async def start(message: types.Message) -> None:
    user_chat_id = str(message.chat.id)
    username = message.from_user.username
    if not username:
        username = message.from_user.full_name

    # add user to database
    db = Database()
    users = [i['chat_id'] for i in db.get_data_list(PROMPT_VIEW_ALL_CHAT_IDS)]
    
    if user_chat_id not in users:
        prompts = get_prompts_add_user(username, user_chat_id)
        db.action(*prompts)
        await _ProfileStatesGroup.get_start_nickname.set()
        with open(START_PHOTO_PATH, 'rb') as file:
            await message.answer_photo(
                photo=types.InputFile(file),
                caption='📍Введите свой Ник'
            )
    else:
        with open(START_PHOTO_PATH, 'rb') as file:
            await message.answer_photo(photo=types.InputFile(file), reply_markup=main_kb)
    


@dp.message_handler(state=_ProfileStatesGroup.get_start_nickname)
async def get_start_nickname(message: types.Message,
                             state: FSMContext) -> None:
    nickname = message.text
    user_chat_id = str(message.chat.id)
    username = message.from_user.username
    if not username:
        username = message.from_user.full_name

    db = Database()
    nicknames = [i['nickname'] for i in db.get_data_list(PROMPT_VIEW_NICKNAMES)]

    if nickname in nicknames:
        await message.answer(
            '❌ Этот Ник уже занят\n📍 Введите другой Ник'
        )
        return
    
    db.action(
        get_prompt_update_nickname(
            chat_id=user_chat_id, new_nick=nickname
        )
    )

    # add user to main sheet
    sm = Stat_mass()
    sm.add_user(user_chat_id, username, nickname)

    # add user to sport types
    sst = Stat_sport_types()
    sst.add_user(user_chat_id)
    
    await state.finish()
    with open(START_PHOTO_PATH, 'rb') as file:
        await message.answer_photo(photo=types.InputFile(file),
                                   reply_markup=main_kb)
    await bot.set_my_commands(
        default_commands, scope=BotCommandScopeChat(message.chat.id)
    )