import pymysql

from .db_config import *



class Database:
    """The class responsible for working with the database of the games and the users"""

    def connect_to_db(self):
        # Connect to the database
        connection = pymysql.connect(
            host=host, user=user, port=3306,
            password=password, database=db_name,
            cursorclass=pymysql.cursors.DictCursor
        )
        return connection


    def action(self, *queries) -> None:
        connection = self.connect_to_db()

        with connection:
            with connection.cursor() as cursor:
                for query in queries:
                    try:
                        cursor.execute(query)
                    except pymysql.err.IntegrityError:
                        connection.rollback()
            connection.commit()


    def get_data_list(self, query: str) -> list[dict[str, int]]:
        connection = self.connect_to_db()
            
        with connection:
            with connection.cursor() as cursor:
                cursor.execute(query)
                data = cursor.fetchall()
        
        return data
    

    def __del__(self) -> None:
        return