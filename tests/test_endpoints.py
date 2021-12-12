import pytest
import requests
import azure.functions as func


# Testing of deployed endpoints from https://not-pirate-bay.azurewebsites.net/docs#

def test_get_movie():
    req = func.HttpRequest(
        method="GET",
        body=None,
        url="/movie/2382320",
    )
    # movie_id = "2382320"
    # movie_result = get_movie_by_id(movie_id=movie_id)
    print(req)
    resp = requests.get(req)
    print(resp)
    # assert movie_result[movie_result][0]["original_title"] == "No Time to Die"

test_get_movie()