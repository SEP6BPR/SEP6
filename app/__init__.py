import azure.functions as func
from azure.functions import AsgiMiddleware
from fastapi import status, HTTPException
from starlette.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_404_NOT_FOUND,
    HTTP_409_CONFLICT,
    HTTP_418_IM_A_TEAPOT,
    HTTP_501_NOT_IMPLEMENTED,
)

from api_app import app
from tmdb_api import get_movie_from_tmdb
from database import (
    get_movie_list_from_email_db,
    get_movie_db,
    sign_up_sign_in_db,
    create_list_for_user_db,
    add_movie_into_list_db,
    get_user_id_db,
)


tags_metadata = [
    {
        "name": "Get movie by ID",
        "description": "Get details about a movie from TMDb API using IMDb id __without__ 'tt*******' format",
    },
    {
        "name": "items",
        "description": "Manage items. So _fancy_ they have their own docs.",
        "externalDocs": {
            "description": "Items external docs",
            "url": "https://fastapi.tiangolo.com/",
        },
    },
]


@app.get("/", status_code=HTTP_200_OK)
def read_root():
    return {"Hello": "Movies"}


@app.get("/movie/{movie_id}", status_code=status.HTTP_200_OK, tags=["Get movie by ID"])
def get_movie_by_id(movie_id: str):
    result = get_movie_db(movie_id)
    if result != "no movie found":
        response, content = get_movie_from_tmdb(result.imdb_id)
    else:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail="Movie with id: {} not found database".format(movie_id),
        )

    if response.status_code != 200:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail="Movie with id: {} not found in TMDB".format(movie_id),
        )
    else:
        return content


@app.get("movie_list/{list_id}", status_code=status.HTTP_200_OK)
def get_movie_list_by_id(list_id: int):
    #TODO
    return {
        "status": "TODO",
        "response": HTTP_418_IM_A_TEAPOT
    }

@app.get("/user/movie_list/{user_email}", status_code=HTTP_200_OK)
def get_users_movie_list(user_email: str):
    tmdb_movies = []
    movie_list = get_movie_list_from_email_db(user_email)
    if movie_list == "no email":
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail="No known user found for email: {}".format(user_email),
        )
    elif movie_list == "no movies for email":
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail="No movies found for email: {}".format(user_email),
        )
    else:
        for movie in movie_list:
            resp, json = get_movie_from_tmdb(movie)
            tmdb_movies.append(json)

        return {"response": HTTP_200_OK, "movies": tmdb_movies}


@app.get("/user/id/{user_email}", status_code=HTTP_200_OK)
def get_user_id(user_email: str):
    return {
        "response": HTTP_200_OK,
        "user_id": get_user_id_db(user_email),
        "user_email": user_email,
    }


@app.post("/user/register/{user_email}", status_code=HTTP_201_CREATED)
def sign_up_sign_in(user_email: str):
    status, user_id = sign_up_sign_in_db(user_email)
    if status == "user creation failed":
        raise HTTPException(
            status_code=HTTP_409_CONFLICT,
            detail="User couldn't be created for email: {}".format(
                user_email
            ),
        )
    else:
        return {
            "response": HTTP_201_CREATED,
            "status": status,
            "user_email": user_email,
            "user_id": user_id,
        }


@app.post("/user/create_list/{user_email}", status_code=HTTP_201_CREATED)
def create_list_for_user(user_email: str):
    user_id = get_user_id_db(user_email)
    user_list = create_list_for_user_db(user_id)
    if user_list == "list not created":
        raise HTTPException(
            status_code=HTTP_409_CONFLICT,
            detail="List couldn't be created for user: {}".format(user_email),
        )
    else:
        return {
            "response": HTTP_201_CREATED,
            "user_email": user_email,
            "movie_list_id": user_list
        }


@app.post("/user/{user_email}/add_to_list/{list_id}")
def add_movie_to_list(user_email: str, list_id: int):
    #TODO
    return {
        "status": "TODO",
        "response": HTTP_418_IM_A_TEAPOT
    }


def main(req: func.HttpRequest, context: func.Context) -> func.HttpResponse:
    return AsgiMiddleware(app).handle(req, context)
