from data_manager import DataManager
from quiz import Quiz

imdb_data = DataManager(
    dbname='imdb',
    user='samaher',
    password="CodingIsFun++",
    host='localhost',
    port='5432'
)

# Get the movie data from the database
movie_data = imdb_data.get_movie()


imdb_data.close_connection()

