import sqlite3
import json


def get_movies(year:int):
    database = sqlite3.connect(database='movies.db')
    print('QUERY: ' + 'SELECT * FROM movies WHERE year={}'.format(year))
    movies = database.execute('SELECT * FROM movies WHERE year={}'.format(year)).fetchall()
    print(json.dumps(movies))


get_movies(2000)

