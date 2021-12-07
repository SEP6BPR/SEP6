import pyodbc


def get_db_cursor():
    connection_string = (
        "Driver={ODBC Driver 13 for SQL Server};"
        "Server=tcp:sep-6.database.windows.net,1433;"
        "Database=movieDatabase;"
        "Uid=michal;"
        "Pwd=sb2Kr7TCzVZM5dF;"
        "Encrypt=yes;"
        "TrustServerCertificate=no;"
        "Connection Timeout=30;"
    )
    connection = pyodbc.connect(connection_string)
    connection.autocommit = True

    cursor = connection.cursor()
    return cursor


def get_movie_list_from_email(email: str):
    movie_ids = []
    db_cursor = get_db_cursor()
    
    db_cursor.execute("SELECT user_id FROM users WHERE email = '{email}'".format(email = email))
    user_id = db_cursor.fetchone().user_id
    # print(user_id)
    db_cursor.execute(
        "SELECT movie_lists.movie_id FROM ((users INNER JOIN user_list_lookup ON users.user_id = {user_id}) INNER JOIN movie_lists ON movie_lists.list_id = user_list_lookup.movie_list_id and user_list_lookup.user_id = {user_id});"
        .format(
            user_id = user_id
        )
    )
    result = db_cursor.fetchall()
    for row in result:
        movie_ids.append(row.movie_id)
    return movie_ids


def get_movie(movie_id: str):
    db_cursor = get_db_cursor()
    db_cursor.execute("SELECT * FROM movies WHERE movie_id = {}".format(movie_id))
    result = db_cursor.fetchone()
    return result


# print(get_movie_list_from_email("e-mail@email.com"))
