from aiogram import types
from aiogram.dispatcher.filters import Command
from database import (Database,
                      get_prompt_add_user,
                      PROMPT_VIEW_ALL_CHAT_IDS)
from ..bot_config import dp
from ..keyboards import main_kb



WELCOME = """
Hello
"""

HELP_TEXT = """
/start - запустить бота
/help - помощь
/voting - голосование
/statistics - статистика
/subscribe - подписаться
"""


@dp.message_handler(Command('start'))
async def start(message: types.Message) -> None:
    user_chat_id = str(message.chat.id)
    username = message.from_user.username
    if not username:
        username = message.from_user.full_name

    db = Database()
    users = [i['chat_id'] for i in db.get_data_list(PROMPT_VIEW_ALL_CHAT_IDS)]

    if not user_chat_id in users:
        db.action(get_prompt_add_user(username, user_chat_id))
        
    await message.answer(WELCOME, reply_markup=main_kb)


@dp.message_handler(Command('help'))
async def help(message: types.Message) -> None:
    await message.answer(HELP_TEXT)