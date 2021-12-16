import os
import sys
from urllib.parse import unquote

from api_app import Review
from fastapi.exceptions import HTTPException
from starlette.status import HTTP_201_CREATED, HTTP_404_NOT_FOUND

sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)))
import logging

import pyodbc
from tmdb_api import fix_movie_id, get_movie_from_tmdb

logging.Logger.root.level = 10


def get_db_cursor() -> pyodbc.Cursor:
    connection_string = os.environ.get("AZURE_SQL_CONNECTION_STRING")
    connection = pyodbc.connect(connection_string)
    connection.autocommit = True

    return connection.cursor()


# Get all movies from email
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
            "SELECT movie_lists.movie_id "
            "FROM ((users INNER JOIN user_list_lookup ON users.user_id = {user_id}) "
            "INNER JOIN movie_lists ON movie_lists.list_id = user_list_lookup.movie_list_id "
            "and user_list_lookup.user_id = {user_id});".format(user_id=user_id)
        )
        result = db_cursor.fetchall()
        for row in result:
            movie_ids.append(row.movie_id)
        return movie_ids

    except Exception as e:
        return "no movies for email"


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
    lists = {}
    user_id = get_user_id_db(user_email)[0]
    db_cursor = get_db_cursor()
    db_cursor.execute(
        "SELECT movie_list_id, list_name FROM user_list_lookup WHERE user_id = {}".format(user_id)
    )
    result = db_cursor.fetchall()

    if result == None:
        return "no lists found"
    else:
        for index, item in enumerate(result):
            if item.list_name == None:
                lists[index] = {
                    "list_name": "Movie List",
                    "list_id": item.movie_list_id
                }
            else:
                lists[index] = {
                    "list_name": item.list_name,
                    "list_id": item.movie_list_id
                }

        return lists


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
            response, content = get_movie_from_tmdb(fix_movie_id(movie_id[0], True))
            movies_from_list.append(content)
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


def create_list_for_user_db(user_id: int, list_name: str = "Movie list"):
    try:
        db_cursor = get_db_cursor()
        db_cursor.execute(
            "INSERT INTO user_list_lookup OUTPUT Inserted.movie_list_id, Inserted.list_name VALUES ({user_id}, '{list_name}')".format(
                user_id=user_id, list_name=unquote(list_name)
            )
        )
        result = db_cursor.fetchone()
    except pyodbc.Error as e:
        logging.error("list creation failed for user: {}".format(user_id))
        return "list not created", ""
    else:
        logging.error(
            "list with id:{list_id} for user: {user_id}".format(
                user_id=user_id, list_id=result.movie_list_id
            )
        )
        return result.movie_list_id, result.list_name


def get_list_name_db(list_id: int):
    db_cursor = get_db_cursor()
    db_cursor.execute(
        "SELECT list_name FROM user_list_lookup WHERE movie_list_id = {}".format(
            list_id
        )
    )
    result = db_cursor.fetchone()
    if result == None:
        return ""
    else:
        return result.list_name


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
                movie_id, movie_list_id
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


def get_top10_movies_from_lists_db():
    top10_movies = []
    db_cursor = get_db_cursor()
    db_cursor.execute(
        "SELECT TOP 10 movie_lists.movie_id, COUNT(movie_lists.movie_id) AS 'count' from movie_lists GROUP BY movie_id ORDER BY COUNT(movie_id) DESC"
    )
    result = db_cursor.fetchall()

    if result != None:
        index = 1
        for row in result:
            response, movie = get_movie_from_tmdb(fix_movie_id(row.movie_id, True))
            movie = {
                "rank": index,
                "no_of_occurences": row.count,
                "movie_data": movie["movie_results"][0],
            }
            top10_movies.append(movie)
            index += 1
        return top10_movies
    else:
        raise pyodbc.Error


def get_reviews_for_movie_db(movie_id: int):

    db_cursor = get_db_cursor()
    db_cursor.execute(
        "SELECT review_id, review_text, user_id, user_name, score, review_date FROM reviews WHERE movie_id = {} ORDER BY review_date DESC".format(
            movie_id
        )
    )
    result = db_cursor.fetchall()

    if result != None:
        reviews = []
        for item in result:
            review = {
                "review_text": item.review_text,
                "user_id": item.user_id,
                "user_name": item.user_name,
                "score": item.score,
                "movie_id": movie_id,
                "review_id": item.review_id,
                "date": item.review_date,
            }
            reviews.append(review)
        return reviews
    else:
        return HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail="No reviews found for movie with id:{}".format(movie_id),
        )


def add_review_for_movie_db(review: Review):
    db_cursor = get_db_cursor()
    db_cursor.execute(
        "INSERT INTO reviews (review_text, user_id, user_name, score, movie_id) OUTPUT Inserted.review_id, Inserted.movie_id VALUES (?,?,?,?,?);",
            review.review_text,
            review.user_id,
            review.user_name,
            review.score,
            review.movie_id,
    )
    result = db_cursor.fetchone()

    if result != None:
        return {
            "response": HTTP_201_CREATED,
            "review_id": result.review_id,
            "movie_id": result.movie_id,
        }
    else:
        return {
            "response": HTTP_404_NOT_FOUND,
        }
