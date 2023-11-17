from data_manager import DataManager
from quiz import quiz_game

imdb_data = DataManager(
    dbname='imdb',
    user='samaher',
    password="CodingIsFun++",
    host='localhost',
    port='5432'
)

# Get the movie data from the database
movie_data = imdb_data.get_movie()

# Execute the quiz game using movie_data
quiz_game(movie_data)

imdb_data.close_connection()
