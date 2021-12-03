import requests
import json

def fix_movie_id(movie_id: int, add_tt: bool):
    movie_id_mod = str(movie_id)

    if len(movie_id_mod) < 8:
        difference = 7 - len(movie_id_mod)
        movie_id_mod = ('0' * difference) + movie_id_mod
    if 'tt' not in movie_id_mod and add_tt is True:
        movie_id_mod = 'tt' + movie_id_mod
    return movie_id_mod

tmdb_api_key = '66ade9da9e0ff7f75853209b4f0b504c'

external_search_URL = 'https://api.themoviedb.org/3/find/{external_id}?api_key={api_key}&external_source=imdb_id'

def get_movie_from_tmdb(imdb_id: int):
    external_id = fix_movie_id(imdb_id, True)
    URL = external_search_URL.format(external_id= external_id, api_key= tmdb_api_key)
    response = requests.get(url = URL)
    content = json.loads(response._content)
    if response.status_code == 200:
        content['movie_results'][0]['id'] = imdb_id
    return response, content

# response, content = get_movie_from_tmdb('tt9603212')

# print(content['movie_results'][0]['id'])

# print(tmdb_movies)