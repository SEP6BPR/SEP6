import pyodbc


# def build_person_search_query(apikey: str, name: str):
#     query = 'https://api.themoviedb.org/3/search/person?api_key={}&query={}'.format(apikey, name)
#     return query
#
#
# def build_movie_search_query(apikey: str, movie: str):
#     query = 'https://api.themoviedb.org/3/search/movie?api_key={}&query={}'.format(apikey, movie)
#     return query
#
# def get_movie(movie_name:str):
#     return True

def get_db_cursor():
    connection_string = 'Driver={ODBC Driver 17 for SQL Server};' \
                        'Server=tcp:sep-6.database.windows.net,1433;' \
                        'Database=movieDatabase;' \
                        'Uid=michal;' \
                        'Pwd=sb2Kr7TCzVZM5dF;' \
                        'Encrypt=yes;' \
                        'TrustServerCertificate=no;' \
                        'Connection Timeout=30;'
    connection = pyodbc.connect(connection_string)
    connection.autocommit = True

    cursor = connection.cursor()
    return cursor
