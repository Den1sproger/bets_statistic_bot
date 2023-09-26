import string

import gspread

from database import SPORT_TYPES
from .config import (SPREADSHEET_ID,
                     CREDENTIALS,
                     STAT_MASS_SPREADSHEET_URL,
                     STAT_SPORTS_SPREADSHEET_URL)



class Connect:
    """Base class for the sheet with the users data"""


    def __init__(self,
                 spreadsheet_url: str,
                 *args, **kwargs) -> None:
        self.gc = gspread.service_account_from_dict(CREDENTIALS,
                                                    client_factory=gspread.BackoffClient)
        self.spreadsheet = self.gc.open_by_key(SPREADSHEET_ID)
        self.worksheet = self.spreadsheet.worksheet(spreadsheet_url)


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
        super().__init__(STAT_MASS_SPREADSHEET_URL)

    
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
        super().__init__(STAT_SPORTS_SPREADSHEET_URL)
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
                        f'{self.__get_column("chat_id", sport_type)}{row}',
                        [[chat_id, 0, 0, 0]]
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

    






