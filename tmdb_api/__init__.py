import requests
import json
import os

tmdb_api_key = os.environ.get("TMDB_API_KEY")

external_search_URL = "https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}"


def fix_movie_id(movie_id: int, add_tt: bool):
    movie_id_mod = str(movie_id)
    if "tt" in movie_id_mod:
        return movie_id_mod
    if len(movie_id_mod) < 8:
        difference = 7 - len(movie_id_mod)
        movie_id_mod = ("0" * difference) + movie_id_mod
    if "tt" not in movie_id_mod and add_tt is True:
        movie_id_mod = "tt" + movie_id_mod
    return movie_id_mod


def get_movie_from_tmdb(movie_id: int):
    URL = external_search_URL.format(movie_id=movie_id, api_key=tmdb_api_key)
    response = requests.get(url=URL)
    content = json.loads(response._content)
    if response.status_code == 200:
        return response, content
