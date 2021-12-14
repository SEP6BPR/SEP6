import sqlite3

import pyodbc
from tqdm import tqdm


def connect_to_db(path: str):
    db = sqlite3.connect(path)
    return db


def fix_movie_id(movie_id: int, add_tt: bool):
    movie_id_mod = str(movie_id)

    if len(movie_id_mod) < 8:
        difference = 7 - len(movie_id_mod)
        movie_id_mod = ('0' * difference) + movie_id_mod
    if 'tt' not in movie_id_mod and add_tt is True:
        movie_id_mod = 'tt' + movie_id_mod
    return movie_id_mod


# Get stuff from a file
cursor = connect_to_db('C:/Users/minco/PycharmProjects/SEP6/Database/movies.db').cursor()

result = cursor.execute("SELECT * FROM movies").fetchall()

index = 0
movies = []
# Transform the ID's into imdb format
for movie_tuple in tqdm(result):
    movie_list = list(movie_tuple)
    movie_list.append(fix_movie_id(movie_list[0], add_tt=False))
    movie_list[0] = fix_movie_id(movie_list[0], add_tt=True)
    # print(movie_list)
    # movie_list.append(index+1)
    movies.append(tuple(movie_list))
    index += 1

print(len(movies))

#
# movie_id_7_count = 0
# movie_id_8_count = 0
# movie_id_9_count = 0
# movie_id_10_count = 0
#
# for movie in movies:
#     # if 'tt' not in movie[0]:
#     #     print(movie)
#
#     if len(movie[0]) == 7:
#         movie_id_7_count += 1
#     elif len(movie[0]) == 8:
#         movie_id_8_count += 1
#     elif len(movie[0]) == 9:
#         movie_id_9_count += 1
#     elif len(movie[0]) == 10:
#         movie_id_10_count += 1
#
# print("Movie with id length 9: {}".format(movie_id_9_count))
# print("Movie with id length 10: {}".format(movie_id_10_count))
# print("Total movies: {}".format(movie_id_9_count+movie_id_10_count))
# print("Movie in list: {}".format(len(movies)))

# Setup Azure DB connection
connection_string = 'Driver={ODBC Driver 13 for SQL Server};' \
                    'Server=tcp:sep-6.database.windows.net,1433;' \
                    'Database=movieDatabase;' \
                    'Uid=michal;' \
                    'Pwd=sb2Kr7TCzVZM5dF;' \
                    'Encrypt=yes;' \
                    'TrustServerCertificate=no;' \
                    'Connection Timeout=30;'
connection = pyodbc.connect(connection_string)
connection.autocommit = True

# Insert ~360k rows into Azure DB.
# !!! TAKES LIKE 3 HOURS TO DO.
cursor = connection.cursor()
for movie in tqdm(movies):
    cursor.execute("insert into movies(imdb_id, movie_name, release_year, movie_id) values (?, ?, ?, ?)", movie)
# cursor.executemany("insert into movies(movie_id, movie_name, release_year, id) values (?, ?, ?, ?)", movies)

# connection.commit()

