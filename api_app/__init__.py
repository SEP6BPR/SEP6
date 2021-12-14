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

class Review(BaseModel):
    review_text: str
    user_id: int
    user_name: str
    score: float
    movie_id: int
