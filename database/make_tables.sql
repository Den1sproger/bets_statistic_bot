CREATE TABLE games
(
	id serial PRIMARY KEY,
    game_key varchar(20) NOT NULL, 
    sport varchar(50) NOT NULL,
    begin_time char(16) NOT NULL,
    first_team varchar(255) NOT NULL,
    first_coeff varchar(10),
    second_team varchar(255) NOT NULL,
    second_coeff varchar(10),
    draw_coeff varchar(10),
	url varchar(255) NOT NULL,
    game_status int NOT NULL,
    poole_first int NOT NULL,
    poole_second int NOT NULL,
    poole_draw int
);


CREATE TABLE users
(
    id serial PRIMARY KEY,
    chat_id varchar(50),
    username varchar(32) NOT NULL,
    positive_bets int NOT NULL,
    negative_bets int NOT NULL,
    roi float NOT NULL,
    team_name varchar(50),
);
-- adding data to the table immediately after creation
INSERT INTO users (username, positive_bets, negative_bets, roi) VALUES ('poole', 0, 0, 0)


CREATE TABLE positive_votes_poole
(
    first_team int NOT NULL,
    second_team int NOT NULL,
    draw int NOT NULL
);
-- adding data to the table immediately after creation
INSERT INTO positive_votes_poole (first_team, second_team, draw) VALUES (0, 0, 0);


CREATE TABLE currents_users_roi
(
    chat_id varchar(50) NOT NULL,
    sport_type varchar(15) NOT NULL,
    positive_bets int NOT NULL,
    negative_bets int NOT NULL,
    roi float NOT NULL,
    CONSTRAINT chat_id_sport_type PRIMARY KEY (chat_id, sport_type)
);


CREATE TABLE answers
(
    chat_id varchar(50) REFERENCES users(chat_id),
    game_key varchar(20) REFERENCES games(game_key),
    answer int NOT NULL,
    CONSTRAINT chat_key PRIMARY KEY (chat_id, game_key)
);


CREATE TABLE current_questions
(
    chat_id varchar(50) PRIMARY KEY,
    current_index int NOT NULL,
    sport_type varchar(255) NOT NULL
);


CREATE TABLE teams
(
    team_name varchar(50) PRIMARY KEY,
    captain_chat_id varchar(50) NOT NULL,
    positive_bets int NOT NULL,
    negative_bets int NOT NULL,
    teammates int NOT NULL,
    roi float NOT NULL
);