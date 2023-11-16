import psycopg2
import pandas as pd

class DataManager:
    def __init__(self, dbname, user, password, host, port):
        self.conn = psycopg2.connect(
            dbname=dbname,
            user=user,
            password=password,
            host=host,
            port=port
        )
        self.cursor = self.conn.cursor()

    def execute_query(self, query):
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def close_connection(self):
        self.cursor.close()
        self.conn.close()

    def get_movie(self):
        query = "SELECT movie.official_title, produced.country, movie.year, rating.votes FROM imdb.produced LEFT JOIN imdb.movie ON produced.movie = movie.id LEFT JOIN imdb.rating ON produced.movie = rating.movie WHERE rating.votes >0 AND movie.year IS NOT NULL;"
        return pd.DataFrame(self.execute_query(query), columns=['official_title', 'country', 'year','votes'])
