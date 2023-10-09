import logging

from aiogram import executor
from telegram_bot import dp, set_default_commands
from telegram_bot.handlers.start import *
from telegram_bot.handlers.voting_menu import *
from telegram_bot.handlers.team_menu import *
from telegram_bot.handlers.default_commands import *



# LOG_FILENAME = "/home/tournament_statistic/py_log.log"
# logging.basicConfig(level=logging.INFO, filename=LOG_FILENAME, filemode="w")

async def on_startup(_):
    await set_default_commands(dp)



if __name__ == '__main__':
    executor.start_polling(dp,
                           skip_updates=True,
                           on_startup=on_startup)
