from aiogram import types
from aiogram.dispatcher.filters import Command
from ..bot_config import dp



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
    await message.answer(WELCOME)


@dp.message_handler(Command('help'))
async def help(message: types.Message) -> None:
    await message.answer(HELP_TEXT)