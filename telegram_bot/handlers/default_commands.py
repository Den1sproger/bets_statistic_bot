from aiogram import types
from aiogram.dispatcher.filters import Command, Text
from ..bot_config import dp


@dp.message_handler(Text(equals='Голосование'))
@dp.message_handler(Command('voting'))
async def voting(message: types.Message) -> None:
    pass



@dp.message_handler(Text(equals='Статистика'))
@dp.message_handler(Command('statistics'))
async def voting(message: types.Message) -> None:
    pass



@dp.message_handler(Text(equals='Подписаться'))
@dp.message_handler(Command('subscribe'))
async def voting(message: types.Message) -> None:
    pass