import os

from aiogram.types import BotCommand
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from dotenv import load_dotenv, find_dotenv



load_dotenv(find_dotenv())

TOKEN = os.getenv('STATISTIC_TOKEN')
bot = Bot(TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())


default_commands = [
    BotCommand('start', 'Запустить бота'),
    BotCommand('help', 'Помощь'),
    BotCommand('voting', 'Голосование'),
    BotCommand('my_team', 'Моя команда'),
    BotCommand('statistics', 'Статистика'),
    BotCommand('nickname', 'Изменить ник'),
    BotCommand('reset_my_stat', 'Обнулить стат')
]