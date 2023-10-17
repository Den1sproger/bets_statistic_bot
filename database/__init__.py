from .db_work import Database


SPORT_TYPES = ('Футбол', 'Хоккей', 'Баскетбол')
PROMPT_VIEW_ALL_CHAT_IDS = "SELECT chat_id FROM users;"
PROMPT_VIEW_NICKNAMES = "SELECT nickname FROM users;"
PROMPT_VIEW_USERNAMES = "SELECT username FROM users;"
PROMPT_VIEW_CURRENT_CHAT_iDS = "SELECT chat_id FROM current_questions;"
PROMPT_VIEW_GAMES = "SELECT * FROM games;"
PROMPT_VIEW_POOLE_STAT = "SELECT positive_bets, negative_bets, roi FROM users WHERE username='poole';"
PROMPT_VIEW_TEAMS = "SELECT team_name FROM teams;"



def get_prompt_update_nickname(chat_id: str | int,
                               new_nick: str) -> str:
    return f"UPDATE users SET nickname='{new_nick}' WHERE chat_id='{chat_id}';"


def get_prompt_update_vote(game_key: str,
                           answer: int,
                           action: str) -> str:
    teams = {
        1: 'poole_first',
        2: 'poole_second',
        3: 'poole_draw'
    }
    return f"UPDATE games SET {teams[answer]}={teams[answer]}{action}1 WHERE game_key='{game_key}';"


def get_prompts_add_user(username: str,
                         chat_id: str) -> list[str]:
    prompts = [f"INSERT INTO users (username, chat_id, positive_bets, negative_bets, coeff_sum, roi) VALUES ('{username}', '{chat_id}', 0, 0, 0, 0);"]
    for sport_type in SPORT_TYPES:
        prompts.append(f"INSERT INTO currents_users_roi (chat_id, sport_type, positive_bets, negative_bets, roi) VALUES ('{chat_id}', '{sport_type}', 0, 0, 0);")
    return prompts


def get_prompt_view_games(sport_type: str) -> str:
    return "SELECT game_key, sport, begin_time, first_team, first_coeff, second_team," \
        f"second_coeff, draw_coeff, url FROM games WHERE game_status=1 AND sport='{sport_type}';"
    

def get_prompt_view_current_info(chat_id: str) -> str:
    return f"SELECT current_index, sport_type FROM current_questions WHERE chat_id='{chat_id}';"


def get_prompt_increase_current_index(chat_id: str) -> str:
    return f"UPDATE current_questions SET current_index=current_index+1 WHERE chat_id='{chat_id}';"


def get_prompt_decrease_current_index(chat_id: str)-> str:
    return f"UPDATE current_questions SET current_index=current_index-1 WHERE chat_id='{chat_id}';"


def get_prompt_update_current_index(chat_id: str,
                                    new_index: int = 0) -> str:
    return f"UPDATE current_questions SET current_index={new_index} WHERE chat_id='{chat_id}';"


def get_prompt_add_current_info(chat_id: str,
                                sport_type: str) -> str:
    return f"INSERT INTO current_questions (chat_id, current_index, sport_type) VALUES ('{chat_id}', 0, '{sport_type}');"


def get_prompt_delete_current_info(chat_id: str) -> str:
    return f"DELETE FROM current_questions WHERE chat_id='{chat_id}';"


def get_prompt_update_current_info(chat_id: str,
                                   sport_type: str,
                                   new_index: int = 0) -> str:
    return f"UPDATE current_questions SET current_index={new_index}, sport_type='{sport_type}' WHERE chat_id='{chat_id}';"


def get_prompt_add_answer(chat_id: str,
                          answer: int,
                          game_key: str) -> str:
    return f"INSERT INTO answers (chat_id, game_key, answer) VALUES ('{chat_id}', '{game_key}', {answer});"


def get_prompt_view_answer(chat_id: str,
                           game_key: str) -> str:
    return f"SELECT answer FROM answers WHERE chat_id='{chat_id}' AND game_key='{game_key}';"


def get_prompt_update_answer(chat_id: str,
                             game_key: str,
                             new_answer: int) -> str:
    return f"UPDATE answers SET answer={new_answer} WHERE chat_id='{chat_id}' AND game_key='{game_key}';"


def get_prompt_view_votes(game_key: str) -> str:
    return f"SELECT poole_first, poole_second, poole_draw FROM games WHERE game_key='{game_key}';"


def get_prompt_increase_current_index(chat_id: str) -> str:
    return f"UPDATE current_questions SET current_index=current_index+1 WHERE chat_id='{chat_id}';"


def get_prompt_decrease_current_index(chat_id: str)-> str:
    return f"UPDATE current_questions SET current_index=current_index-1 WHERE chat_id='{chat_id}';"


def get_prompt_view_user_stat(chat_id: str) -> str:
    return f"SELECT positive_bets, negative_bets, roi FROM users WHERE chat_id='{chat_id}';"


def get_prompt_view_user_team(chat_id: str) -> str:
    return f"SELECT team_name FROM users WHERE chat_id='{chat_id}';"


def get_prompt_view_team_stat(team_name: str) -> str:
    return f"SELECT positive_bets, negative_bets, roi FROM teams WHERE team_name='{team_name}';"


def get_prompt_view_teammates(team_name: str,
                              captain_chat_id: str) -> str:
    return f"SELECT * FROM users WHERE team_name='{team_name}' AND chat_id <> '{captain_chat_id}';"


def get_prompt_view_captain(team_name: str) -> str:
    return f"SELECT captain_chat_id FROM teams WHERE team_name='{team_name}';"


def get_prompt_create_team(team_name: str,
                           captain: str) -> list[str]:
    return (
        f"INSERT INTO teams (team_name, captain_chat_id, positive_bets, negative_bets, roi, teammates)" \
        f"VALUES ('{team_name}', '{captain}', 0, 0, 0, 1);",
        f"UPDATE users SET team_name='{team_name}' WHERE chat_id='{captain}';"
    )


def get_prompt_view_username_by_id(chat_id: str) -> str:
    return f"SELECT username FROM users WHERE chat_id='{chat_id}';"


def get_prompt_view_nickname_by_id(chat_id: str) -> str:
    return f"SELECT nickname FROM users WHERE chat_id='{chat_id}';"


def get_prompt_view_chat_id_by_name(username: str) -> str:
    return f"SELECT chat_id FROM users WHERE username='{username}';"


def get_prompt_view_chat_id_by_nick(nickname: str) -> str:
    return f"SELECT chat_id FROM users WHERE nickname='{nickname}';"


def get_prompt_view_team_size(team_name: str) -> str:
    return f"SELECT teammates FROM teams WHERE team_name='{team_name}';"


def get_prompts_leave_team(chat_id: str,
                           team_name: str) -> str:
    return (
        f"UPDATE users SET team_name=NULL WHERE chat_id='{chat_id}';",
        f"UPDATE teams SET teammates=teammates=teammates-1 WHERE team_name='{team_name}'"
    )


def get_prompts_add_teammate(chat_id: str,
                             team_name: str) -> str:
    return (
        f"UPDATE users SET team_name='{team_name}' WHERE chat_id='{chat_id}';",
        f"UPDATE teams SET teammates=teammates+1 WHERE team_name='{team_name}'"
    )


def get_prompts_delete_team(team_name: str) -> list[str]:
    return (
        f"DELETE FROM teams WHERE team_name='{team_name}';",
        f"UPDATE users SET team_name=NULL WHERE team_name='{team_name}';"
    )


def get_prompt_update_game_status(game_key: str,
                                  status: int) -> str:
    return f"UPDATE games SET game_status={status} WHERE game_key='{game_key}';"



__all__ = [
    'Database',
    'SPORT_TYPES',
    'PROMPT_VIEW_NICKNAMES',
    'PROMPT_VIEW_ALL_CHAT_IDS',
    'PROMPT_VIEW_CURRENT_CHAT_iDS',
    'PROMPT_VIEW_GAMES',
    'PROMPT_VIEW_POOLE_STAT',
    'PROMPT_VIEW_TEAMS',
    'PROMPT_VIEW_USERNAMES',
    'get_prompt_update_nickname',
    'get_prompt_update_vote',
    'get_prompts_add_user',
    'get_prompt_view_games',
    'get_prompt_view_current_info',
    'get_prompt_increase_current_index',
    'get_prompt_decrease_current_index',
    'get_prompt_add_current_info',
    'get_prompt_update_current_index',
    'get_prompt_delete_current_info',
    'get_prompt_update_current_info',
    'get_prompt_add_answer',
    'get_prompt_view_answer',
    'get_prompt_update_answer',
    'get_prompt_view_votes',
    'get_prompt_increase_current_index',
    'get_prompt_decrease_current_index',
    'get_prompt_view_user_stat',
    'get_prompt_view_user_team',
    'get_prompt_view_team_stat',
    'get_prompt_view_teammates',
    'get_prompt_view_captain',
    'get_prompt_create_team',
    'get_prompt_leave_team',
    'get_prompt_add_teammate',
    'get_prompt_view_username_by_id',
    'get_prompt_view_nickname_by_id',
    'get_prompt_view_chat_id_by_name',
    'get_prompt_view_chat_id_by_nick',
    'get_prompt_view_team_size',
    'get_prompt_update_game_status'
]