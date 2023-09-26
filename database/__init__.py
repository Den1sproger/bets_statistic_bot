from .db_work import Database


SPORT_TYPES = ('SOCCER', 'HOCKEY', 'BASKETBALL')
PROMPT_VIEW_ALL_CHAT_IDS = "SELECT chat_id FROM users;"
PROMPT_VIEW_CURRENT_CHAT_iDS = "SELECT chat_id FROM current_questions;"



def get_prompt_add_user(username: str,
                        chat_id: str) -> str:
    return f"INSERT INTO users (username, chat_id, positive_bets, negative_bets, roi)" \
            f"VALUES ('{username}', '{chat_id}', 0, 0, 0);"


def get_prompt_view_games(sport_type: str) -> str:
    return "SELECT game_key, sport, begin_time, first_team, first_coeff, second_team," \
        f"second_coeff, draw_coeff, url FROM games WHERE game_status=1 AND sport='{sport_type}';"
    

def get_prompt_view_current_info(chat_id: str) -> str:
    return f"SELECT current_index FROM current_questions WHERE chat_id='{chat_id}';"


def get_prompt_increase_current_index(chat_id: str) -> str:
    return f"UPDATE current_questions SET current_index=current_index+1 WHERE chat_id='{chat_id}';"


def get_prompt_decrease_current_index(chat_id: str)-> str:
    return f"UPDATE current_questions SET current_index=current_index-1 WHERE chat_id='{chat_id}';"


def get_prompt_update_current_index(chat_id: str,
                                    new_index: int) -> str:
    return f"UPDATE current_questions SET current_index={new_index} WHERE chat_id='{chat_id}';"


def get_prompt_add_current_info(chat_id: str) -> str:
    return f"INSERT INTO current_questions (chat_id, current_index) VALUES ('{chat_id}', 0);"


def get_prompt_delete_current_info(chat_id: str) -> str:
    return f"DELETE FROM current_questions WHERE chat_id='{chat_id}';"


def get_prompt_add_answer(chat_id: str,
                          answer: int,
                          game_key: str) -> str:
    return f"INSERT INTO answers (chat_id, game_key, tournament, answer) VALUES ('{chat_id}', '{game_key}', {answer});"


def get_prompt_view_answer(chat_id: str,
                           game_key: str) -> str:
    return f"SELECT answer FROM answers WHERE chat_id='{chat_id}' AND game_key='{game_key}';"


def get_prompt_update_answer(chat_id: str,
                             game_key: str,
                             new_answer: int) -> str:
    return f"UPDATE answers SET answer={new_answer} WHERE chat_id='{chat_id}' AND game_key='{game_key}';"



__all__ = [
    'Database',
    'SPORT_TYPES',
    'PROMPT_VIEW_ALL_CHAT_IDS',
    'PROMPT_VIEW_CURRENT_CHAT_iDS',
    'get_prompt_add_user',
    'get_prompt_view_games',
    'get_prompt_view_current_info',
    'get_prompt_increase_current_index',
    'get_prompt_decrease_current_index',
    'get_prompt_add_current_info',
    'get_prompt_update_current_index',
    'get_prompt_delete_current_info',
    'get_prompt_add_answer',
    'get_prompt_view_answer',
    'get_prompt_update_answer',
]