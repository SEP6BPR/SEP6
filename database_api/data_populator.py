# import database_api
import sys, os
import random
import pyodbc
from tqdm import tqdm

sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)))


def get_db_cursor() -> pyodbc.Cursor:
    connection_string = ""
    # print(connection_string)
    connection = pyodbc.connect(connection_string)
    connection.autocommit = True

    return connection.cursor()


def insert(list_id, movie_id):
    db_cursor = get_db_cursor()
    # print("list:{} \n movie:{}".format(list_id,movie_id))
    db_cursor.execute(
        "INSERT INTO movie_lists OUTPUT Inserted.movie_id, Inserted.list_id VALUES ({list_id},{movie_id})".format(
            list_id=list_id, movie_id=movie_id
        )
    )

    return db_cursor.fetchone()


movies = {
    1: 7131622,  # "Once Upon a Time... In Hollywood"
    2: 1160419,  # "Dune"
    3: 816692,  # "Interstellar"
    4: 111161,  # "The Shawshank Redemption"
    5: 361748,  # "Inglourious Basterds"
    6: 133093,  # "The Matrix"
    7: 468569,  # "The Dark Knight"
    8: 167260,  # "The Lord of the Rings: The Return of the King"
    9: 110912,  # "Pulp Fiction"
    10: 76759,  # "Star Wars: Episode IV - A New Hope"
}

# random.seed(1)
def insert_movies_in_list(list_id: int, movies: dict):
    for index, number in enumerate(tqdm(range(1, 6))):
        movies_added = []

        random_movie = random.randint(1, 10)
        # print(random_movie)
        while random_movie in movies_added:
            random_movie = random.randint(1, 10)
            # print("in loop:" + random_movie)

        try:
            result = insert(list_id, movies[random_movie])
            movies_added.append(result.movie_id)
        except pyodbc.IntegrityError:
            continue
    # print(result)


insert_movies_in_list(list_id=24, movies=movies)
# print(len(movies))
