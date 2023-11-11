from data import DataManager

imdb_data = DataManager(
    dbname='imdb',
    user='samaher',
    password="CodingIsFun++",
    host='localhost',
    port='5432'
)

# Get data for movie release years
movie_data = imdb_data.get_movie()
print("Movie Release Years:")
print(movie_data)

# Get data for movie genres
genre_data = imdb_data.get_genre_movie()
print("\nMovie Genres:")
print(genre_data)


# Close the connection when done
imdb_data.close_connection()
