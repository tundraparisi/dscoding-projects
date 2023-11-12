from data import DataManager

# Opening the connection
imdb_data = DataManager(
    dbname='imdb',
    user='samaher',
    password="CodingIsFun++",
    host='localhost',
    port='5432'
)




# Closing the connection
imdb_data.close_connection()
