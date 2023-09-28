import string

import gspread

from database import (Database,
                      PROMPT_VIEW_GAMES,
                      SPORT_TYPES,
                      get_prompt_view_votes)
from .config import (SPREADSHEET_ID,
                     CREDENTIALS,
                     STAT_MASS_SPREADSHEET_URL,
                     STAT_SPORTS_SPREADSHEET_URL)



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
        "positive_bets": "C",
        "negative_bets": "D",
        "roi": "E"
    }
    SHEET_NAME = "Статы массовые"


    def __init__(self, *args, **kwargs):
        super().__init__()
        self.worksheet = self.spreadsheet.worksheet(self.SHEET_NAME)
    

    def add_user(self,
                 chat_id: str,
                 username: str) -> None:
        # add user in table
        chat_ids = self.worksheet.col_values(1)
        if chat_id not in chat_ids:
            row = len(chat_ids) + 1
            self.worksheet.update(
                f'{self.CELLS_COLS["chat_id"]}{row}',
                [[chat_id, username, 0, 0, 0]]
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

        if sport_type == 'SOCCER':
            return self.CELLS_COLS[column]
        elif sport_type == 'HOCKEY':
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

    
    # def reset_votes(self):
    #     update_data = []

    #     for sport_type in SPORT_TYPES:
    #         update_data.append(
    #             {
    #                 f'{self.__get_column("positive_bets", sport_type)}2:{self.__get_column("negative_bets")}{row}',
    #                 [[chat_id, username, 0, 0, 0]]
    #             }
    #         ) 
    #     self.worksheet.batch_update(update_data)


class Games(Connect):
    """"""

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


    def update_votes(self, team_name: str, game_data: dict) -> None:
        db = Database()
        games = db.get_data_list(PROMPT_VIEW_GAMES)

        game_key = game_data['game_key']

        count = 1
        votes: int

        for game in games:
            teams = len(game['coeffs'])

            if game['game_key'] == game_key:

                for team, db_key in zip(game['coeffs'], ('poole_first', 'poole_second', 'poole_draw')):
                    count += 1
                    if team == team_name:
                        votes = game[db_key]
                        break

                break
            count += teams
            
        self.worksheet.update(f"{self.CELLS_COLS['poole']}{count}", votes)




        