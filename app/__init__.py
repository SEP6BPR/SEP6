import azure.functions as func
from azure.functions import AsgiMiddleware
from fastapi import status, HTTPException
from starlette.status import HTTP_404_NOT_FOUND

from api_app import app
from tmdb_api import get_movie_from_tmdb
from database import get_movie_list_from_email, get_movie



@app.get("/")
def read_root():
    return {"Hello": "Movies"}


@app.get("/movie/{movie_id}", status_code=status.HTTP_200_OK)
def get_movie_by_id(movie_id: str):
    result = get_movie(movie_id)
    if result != "no movie found":
        response, content = get_movie_from_tmdb(result.imdb_id)
    else:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="Movie with id: {} not found database".format(movie_id))

    if response.status_code != 200:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="Movie with id: {} not found in TMDB".format(movie_id))
    else:
        return content


@app.get("/user/movie_list/{user_email}")
def get_users_movie_list(user_email: str):
    tmdb_movies = []
    movie_list = get_movie_list_from_email(user_email)
    if movie_list is not list:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="No movies found for email: {}".format(user_email))
    else:
        for movie in movie_list:
            resp, json = get_movie_from_tmdb(movie)
            tmdb_movies.append(json)    

        return {
            "movies": tmdb_movies
        }


def main(req: func.HttpRequest, context: func.Context) -> func.HttpResponse:
    return AsgiMiddleware(app).handle(req, context)
