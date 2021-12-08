import sys
import os

sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)))
import pyodbc
import logging

logging.Logger.root.level = 10


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


def get_movie_list_from_email_db(email: str):
    movie_ids = []
    db_cursor = get_db_cursor()
    try:
        db_cursor.execute(
            "SELECT user_id FROM users WHERE email = '{email}'".format(email=email)
        )
        user_id = db_cursor.fetchone().user_id
    except Exception as e:
        return "no email"
    try:
        db_cursor.execute(
            "SELECT movie_lists.movie_id FROM ((users INNER JOIN user_list_lookup ON users.user_id = {user_id}) INNER JOIN movie_lists ON movie_lists.list_id = user_list_lookup.movie_list_id and user_list_lookup.user_id = {user_id});".format(
                user_id=user_id
            )
        )
        result = db_cursor.fetchall()
        for row in result:
            movie_ids.append(row.movie_id)
        return movie_ids

    except Exception as e:
        return "no movies for email"


def get_movie_db(movie_id: str):
    try:
        db_cursor = get_db_cursor()
        db_cursor.execute("SELECT * FROM movies WHERE movie_id = {}".format(movie_id))
        result = db_cursor.fetchone()
    except Exception as e:
        logging.error("movie lookup failed for movie_id: {}".format(movie_id))
        return "no movie found"
    else:
        return result


def get_user_id_db(user_email: str):
    try:
        db_cursor = get_db_cursor()
        db_cursor.execute(
            "SELECT user_id FROM users WHERE email = '{}'".format(user_email)
        )
        result = db_cursor.fetchone()

        if result == None:
            return None
        else:
            return result
    except Exception as e:
        # TODO add better error handling
        logging.error("cant get user_id for email: {}".format(user_email))
        return "get_user_id failed"


def sign_up_sign_in_db(user_email: str):

    db_cursor = get_db_cursor()
    db_cursor.execute("SELECT user_id FROM users WHERE email = '{}'".format(user_email))
    result = db_cursor.fetchone()

    if result == None:
        db_cursor.execute(
            "INSERT INTO users OUTPUT Inserted.user_id VALUES('{}');".format(user_email)
        )
        result = db_cursor.fetchone()
        print(result)
        return "user created", result.user_id
    else:
        return "user retrieved", result.user_id

    # try:
    #     db_cursor = get_db_cursor()
    #     db_cursor.execute(
    #         "INSERT INTO users OUTPUT Inserted.user_id VALUES('{}');".format(user_email)
    #     )
    #     result = db_cursor.fetchone()
    #     print(result)
    #     return "user created", result.user_id

    # except Exception as e:
    #     # TODO add better error handling

    #     try:
    #         user_id = get_user_id_db(user_email)
    #     except pyodbc.Error as e:
    #         logging.error("user creation failed for email: {}".format(user_email))
    #         return "user creation failed", ""
    #     else:
    #         return "user retrieved", user_id
    # else:
    #     logging.error("user with email:{} created".format(user_email))
    #     return "user created", get_user_id_db(user_email)


def get_lists_for_user(user_email: str):
    user_id = get_user_id_db(user_email)


def create_list_for_user_db(user_id: int):
    try:
        db_cursor = get_db_cursor()
        print(user_id)
        db_cursor.execute(
            "INSERT INTO user_list_lookup OUTPUT Inserted.movie_list_id VALUES ({})".format(
                user_id
            )
        )
        result = db_cursor.fetchone()
        print(result)
    except pyodbc.Error as e:
        print(e)
        logging.error("list creation failed for user: {}".format(user_id))
        return "list not created"
    else:
        logging.error(
            "list with id:{list_id} for user: {user_id}".format(
                user_id=user_id, list_id=result.movie_list_id
            )
        )
        return result.movie_list_id


def add_movie_into_list_db(movie_list_id: int, movie_id: int):
    try:
        db_cursor = get_db_cursor()
        db_cursor.execute(
            "INSERT INTO movie_lists OUTPUT Inserted.movie_id, Inserted.list_id VALUES ({list_id},{movie_id})".format(
                list_id=movie_list_id, movie_id=movie_id
            )
        )
        result = db_cursor.fetchone()
    except pyodbc.Error as e:
        logging.error(
            "adding movie with id:{} failed for list with id: {}".format(
                movie_list_id, movie_id
            )
        )
    else:
        logging.error(
            "added movie with id:{movie_id} into list with id: {list_id}".format(
                movie_id=movie_id, list_id=movie_list_id
            )
        )
        return result.movie_list_id


def remove_movie_from_list_db(movie_list_id: int, movie_id: int):
    return True


# print(create_user("285056@viauc.dk"))
