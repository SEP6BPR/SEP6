import azure.functions as func
from azure.functions import AsgiMiddleware

from api_app import app
import pyodbc
import mimesis



def get_db_cursor():
    connection_string = (
        "Driver={ODBC Driver 17 for SQL Server};"
        "Server=tcp:sep-6.database.windows.net,1433;"
        "Database=movieDatabase;"
        "Uid=michal;"
        "Pwd=sb2Kr7TCzVZM5dF;"
        "Encrypt=yes;"
        "TrustServerCertificate=no;"
        "Connection Timeout=30;"
    )
    connection = pyodbc.connect(connection_string)
    connection.autocommit = True

    cursor = connection.cursor()
    return cursor





@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/movie/{id}")
def get_movie(id: str):
    db_cursor = get_db_cursor()
    db_cursor.execute("SELECT * FROM movies WHERE id = {}".format(id))
    result = db_cursor.fetchone()
    # result = mimesis.Person()
    if result is not None:
        return {
            "movieid": result.movie_id,
            "movie_name": result.movie_name,
            "release_year": result.release_year,
            "id": result.id,
        }
    else:
        return {"message": "Movie not found"}


def main(req: func.HttpRequest, context: func.Context) -> func.HttpResponse:
    return AsgiMiddleware(app).handle(req, context)
