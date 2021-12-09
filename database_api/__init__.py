import sys
import os

sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)))
import pyodbc
import logging
from tmdb_api import get_movie_from_tmdb

logging.Logger.root.level = 10


def get_db_cursor():
    connection_string = os.environ.get("AZURE_SQL_CONNECTION_STRING")
    connection = pyodbc.connect(connection_string)
    connection.autocommit = True

    cursor = connection.cursor()
    return cursor


# Get all movies
def get_movies_from_email_db(email: str):
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
        logging.error("cant get user_id for email: {}".format(user_email))
        return "get_user_id failed"


# Get list_id's associated to the user's email
def get_users_lists_db(user_email: str):
    list_ids = {}
    user_id = get_user_id_db(user_email)[0]
    db_cursor = get_db_cursor()
    db_cursor.execute(
        "SELECT movie_list_id FROM user_list_lookup WHERE user_id = {}".format(user_id)
    )
    result = db_cursor.fetchall()

    if result == None:
        return "no lists found"
    else:
        for item in result:
            # list_ids.append(item[0])
            db_cursor.execute(
                "SELECT movie_id FROM movie_lists WHERE list_id = {}".format(item[0])
            )
            movies = db_cursor.fetchall()

            if movies == None:
                return "no movies found"
            else:
                list_ids[item[0]] = []
                for movie_id in movies:
                    list_ids[item[0]].append(movie_id[0])

        return list_ids


def get_movies_from_list_db(list_id: int):
    movies_from_list = []

    db_cursor = get_db_cursor()
    db_cursor.execute(
        "SELECT movie_id FROM movie_lists WHERE list_id = {}".format(list_id)
    )
    result = db_cursor.fetchall()

    if result == None:
        return "no movies in list"
    else:
        for movie_id in result:
            movies_from_list.append(get_movie_from_tmdb(movie_id))

        return movies_from_list


def sign_up_sign_in_db(user_email: str):

    db_cursor = get_db_cursor()
    db_cursor.execute("SELECT user_id FROM users WHERE email = '{}'".format(user_email))
    result = db_cursor.fetchone()

    if result == None:
        db_cursor.execute(
            "INSERT INTO users OUTPUT Inserted.user_id VALUES('{}');".format(user_email)
        )
        result = db_cursor.fetchone()
        return "user created", result.user_id
    else:
        return "user retrieved", result.user_id


def create_list_for_user_db(user_id: int):
    try:
        db_cursor = get_db_cursor()
        db_cursor.execute(
            "INSERT INTO user_list_lookup OUTPUT Inserted.movie_list_id VALUES ({})".format(
                user_id
            )
        )
        result = db_cursor.fetchone()
    except pyodbc.Error as e:
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
    except Exception as e:
        logging.error(
            "adding movie with id:{} failed for list with id: {}".format(
                movie_list_id, movie_id
            )
        )
        return "movie not added"
    else:
        logging.error(
            "added movie with id:{movie_id} into list with id: {list_id}".format(
                movie_id=movie_id, list_id=movie_list_id
            )
        )
        return result.movie_list_id


def remove_movie_from_list_db(movie_list_id: int, movie_id: int):
    try:
        db_cursor = get_db_cursor()
        db_cursor.execute(
            "DELETE FROM movie_lists WHERE list_id = {list_id} and movie_id = {movie_id}".format(
                list_id=movie_list_id, movie_id=movie_id
            )
        )
    except Exception as e:
        logging.error(
            "removing movie with id:{} failed for list with id: {}".format(
                movie_list_id, movie_id
            )
        )
        return "movie not removed"
    else:
        logging.error(
            "removed movie with id:{movie_id} into list with id: {list_id}".format(
                movie_id=movie_id, list_id=movie_list_id
            )
        )
        return "movie removed"
