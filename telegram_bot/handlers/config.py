from aiogram.dispatcher.filters.state import State, StatesGroup



class _ProfileStatesGroup(StatesGroup):
    get_team_name = State()
    get_nickname_for_team = State()
    get_start_nickname = State()