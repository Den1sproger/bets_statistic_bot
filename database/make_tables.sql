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
);

CREATE TABLE users
(
	id serial PRIMARY KEY,
    username varchar(32) NOT NULL,
    chat_id varchar(50) NOT NULL,
);

CREATE TABLE answers
(
    chat_id varchar(50) REFERENCES users(chat_id),
    game_key varchar(20) REFERENCES games(game_key),
    answer int NOT NULL,
    CONSTRAINT chat_key_tourn PRIMARY KEY (chat_id, game_key)
);

CREATE TABLE current_questions
(
    chat_id varchar(50) PRIMARY KEY,
    current_index int NOT NULL
);