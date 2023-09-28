from aiogram import types
from aiogram.dispatcher.filters import Command, Text
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
async def subscribe(message: types.Message) -> None:
    pass


@dp.message_handler(Text(equals='Статистика'))
@dp.message_handler(Command('statistics'))
async def statistics(message: types.Message) -> None:
    pass