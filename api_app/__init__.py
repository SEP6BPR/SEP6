import fastapi
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel


app = fastapi.FastAPI()

# FastAPI config will go here if needed
origins = [
    "http://localhost:3000/",
    "http://localhost:8080",
]
origins_allow_all = ['*']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins_allow_all,
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Movie(BaseModel):
    title: str = "No Time to Die"
    vote_average: float = 7.6
    overview: str = "Bond has left active service and is enjoying a tranquil life in Jamaica. His peace is short-lived when his old friend Felix Leiter from the CIA turns up asking for help. The mission to rescue a kidnapped scientist turns out to be far more treacherous than expected, leading Bond onto the trail of a mysterious villain armed with dangerous new technology."
    release_date: str = "2021-09-29"
    adult: bool = False
    backdrop_path: str = "/dnxrremCrghG7z97zDeGPNrl75A.jpg"
    vote_count: int = 2488
    genre_ids: list = [
        12,
        28,
        53
    ]
    id: str = "tt2382320"
    original_language: str = "en"
    original_title: str = "No Time to Die"
    poster_path: str = "/iUgygt3fscRoKWCV1d0C7FbM9TP.jpg"
    video: bool = False
    popularity: float = 1742.817
    

class MovieResult(Movie):
    movie_results: list[Movie]
    person_results: list[dict]
    tv_results: list[dict]
    tv_episode_results: list[dict]
    tv_season_results: list[dict]