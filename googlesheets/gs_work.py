import string

import gspread

from database import (Database,
                      PROMPT_VIEW_GAMES,
                      SPORT_TYPES)
from .config import SPREADSHEET_ID, CREDENTIALS




class Connect:
    """Base class for the sheet with the users data"""


    def __init__(self, *args, **kwargs) -> None:
        self.gc = gspread.service_account_from_dict(CREDENTIALS,
                                                    client_factory=gspread.BackoffClient)
        self.spreadsheet = self.gc.open_by_key(SPREADSHEET_ID)
        

    def __del__(self):
        return


    

class Stat_mass(Connect):
    """Class for the work with the data in the worksheet with the all users"""

    CELLS_COLS = {
        "chat_id": "A",
        "username": "B",
        "nickname": "C",
        "positive_bets": "D",
        "negative_bets": "E",
        "roi": "F",
        "coeff_sum": "G"
    }
    SHEET_NAME = "Статы массовые"


    def __init__(self, *args, **kwargs):
        super().__init__()
        self.worksheet = self.spreadsheet.worksheet(self.SHEET_NAME)
    

    def add_user(self, chat_id: str, username: str, nickname: str) -> None:
        # add user to table
        chat_ids = self.worksheet.col_values(1)
        if chat_id not in chat_ids:
            row = len(chat_ids) + 1
            self.worksheet.update(
                f'{self.CELLS_COLS["chat_id"]}{row}',
                [[chat_id, username, nickname, 0, 0, 0, 0]]
            )

    
    def update_nickname(self, new_nick: str, chat_id: str) -> None:
        cell = self.worksheet.find(chat_id, in_column=1)
        self.worksheet.update_cell(row=cell.row, col=3, value=new_nick)


    def reset_user_stat(self, chat_id: str | int) -> None:
        cell = self.worksheet.find(chat_id, in_column=1)
        self.worksheet.update(
            f"{self.CELLS_COLS['positive_bets']}{cell.row}",
            [[0, 0, 0, 0]]
        )




class Stat_sport_types(Connect):
    """Class for the work with the data in the worksheet with the users and sport types"""

    CELLS_COLS = {
        "chat_id": "A",
        "positive_bets": "B",
        "negative_bets": "C",
        "roi": "D"
    }
    SHEET_NAME = "Стат виды спорта"
    LENGTH = len(CELLS_COLS)
    BETWEEN = 1
    OFFSET = LENGTH + BETWEEN


    def __init__(self, *args, **kwargs):
        super().__init__()
        self.worksheet = self.spreadsheet.worksheet(self.SHEET_NAME)
        self.cells = string.ascii_uppercase


    def __get_column(self,
                     column: str,
                     sport_type: str) -> str:
        assert sport_type in SPORT_TYPES, 'Unknown sport type'

        if sport_type == 'Футбол':
            return self.CELLS_COLS[column]
        elif sport_type == 'Хоккей':
            return self.cells[self.cells.index(self.CELLS_COLS[column]) + self.OFFSET]
        else:
            return self.cells[self.cells.index(self.CELLS_COLS[column]) + self.OFFSET * 2]


    def add_user(self, chat_id: str) -> None:
        # add user in table
        chat_ids = self.worksheet.col_values(1)
        if chat_id not in chat_ids:
            row = len(chat_ids) + 1

            update_data = []

            for sport_type in SPORT_TYPES:
                update_data.append(
                    {
                        'range': f'{self.__get_column("chat_id", sport_type)}{row}',
                        'values': [[chat_id, 0, 0, 0]]
                    }
                )
            self.worksheet.batch_update(update_data)


    def reset_user_stat(self, chat_id: str | int) -> None:
        cell_soccer = self.worksheet.find(chat_id, in_column=1)
        cell_hockey = self.worksheet.find(chat_id, in_column=6)
        cell_basketball = self.worksheet.find(chat_id, in_column=11)

        update_data = []

        for sport_type, cell in zip(SPORT_TYPES, (cell_soccer, cell_hockey, cell_basketball)):
            update_data.append(
                {
                    'range': f'{self.__get_column("positive_bets", sport_type)}{cell.row}',
                    'values': [[0, 0, 0]]
                }
            )
        
        self.worksheet.batch_update(update_data)




class Games(Connect):
    """Class for the work with the games in googlesheet"""

    CELLS_COLS = {
        'game_number': 'A',
        'sport': 'B',
        'begin_time': 'C',
        'teams': 'D',
        'coefficients': 'E',
        'url': 'F',
        'poole': 'G'
    }
    SHEET_NAME = 'Матчи'


    def __init__(self, *args, **kwargs):
        super().__init__()
        self.worksheet = self.spreadsheet.worksheet(self.SHEET_NAME)


    def update_votes(self, game_key: str) -> None:
        # update votes in the last column for the one team
        db = Database()
        games = db.get_data_list(PROMPT_VIEW_GAMES)

        count = 2
        votes = []

        for game in games:
            teams = [[game['poole_first']], [game['poole_second']]]
            draw = game['poole_draw']

            if draw != None:
                teams.append([draw])       # add draw poole

            if game['game_key'] == game_key:
                votes = teams
                break
            
            count += len(teams)
            
        self.worksheet.update(f"{self.CELLS_COLS['poole']}{count}", votes)