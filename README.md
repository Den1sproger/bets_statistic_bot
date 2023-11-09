# Tournament statistics bot

This is a Telegram bot for maintaining betting statistics.

In this bot, the user is invited to vote for the outcome of the proposed sports matches. The user can vote for the first team, for the second and for a draw. Sports matches are selected by the administrator in his [administrative bot](https://github.com/Den1sproger/statisctics-admin-bot "Admin bot repository").

Statistics are kept on user votes:
1. User personal statistics
2. Poole statistics
3. Team statistics

***Poole statistics*** - Statistics of the total number of all users.

***Team statistics*** - A user can create his own team of up to 10 people and can be invited to an already created team. If the user is a member of a team, the statistics of this team are calculated.

## To start
### Clone this repository
```
git clone https://github.com/Den1sproger/bets_statistic_bot.git
```

### Create virtual environment

Windows:
```
python -m venv venv
```

Linux\Mac OS:
```
python3 -m venv venv
```

### Install dependencies

Windows:
```
pip install -r requirements.txt
```

Linux\Mac OS:
```
pip3 install -r requirements.txt
```

### Create MySQL Database
```
CREATE DATABASE statistics;
```

Save **db_name**, **password**, **user** and **host** to environment variables under the same names.

#### Create db tables
See SQL file => [make_tables.sql](https://github.com/Den1sproger/bets_statistic_bot/blob/main/database/make_tables.sql "make tables sql file")

### Create GoogleSheets


### Create Telegram Bot
Go to [BotFather](https://t.me/BotFather "Bot Father") and create bot. Save API TOKEN to environment variable under the name **STATISTIC_TOKEN**

### Launch main file
Windows:
```
python app.py
```

Linux\Mac OS:
```
python3 app.py
```

## Admin Telegram bot
For the normal operation of this bot, it is necessary to activate the administrative bot.

[Administrative bot Repo](https://github.com/Den1sproger/statisctics-admin-bot "Admin bot repository")