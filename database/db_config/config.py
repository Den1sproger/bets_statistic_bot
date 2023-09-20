import os

from dotenv import load_dotenv, find_dotenv


load_dotenv(find_dotenv())

host = os.getenv('host')
user = os.getenv('user')
password = os.getenv('password')
db_name = os.getenv('db_statistic_name')