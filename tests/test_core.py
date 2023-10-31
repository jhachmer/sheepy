# Desc: Unit tests for core.py
# flake8: noqa
from unittest.mock import patch
import pytest
import requests

from sheepy.core import get_movie_data


@patch('sheepy.core.requests.get')
def test_get_movie_data_success(mock_get):
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {
        "Title": "The Matrix",
        "Year": "1999",
        "Rated": "R",
        "Released": "31 Mar 1999",
        "Runtime": "136 min",
        "Genre": "Action, Sci-Fi",
        "Director": "Lana Wachowski, Lilly Wachowski",
        "Writer": "Lilly Wachowski, Lana Wachowski",
        "Actors": "Keanu Reeves, Laurence Fishburne, "
                  "Carrie-Anne Moss, Hugo Weaving",
        "Plot": "A computer hacker learns from mysterious "
                "rebels about the true nature of his reality "
                "and his role in the war against its controllers.",
        "Language": "English",
        "Country": "USA",
        "Awards": "Won 4 Oscars. Another 37 wins & 51 nominations.",
        "Poster": "https://m.media-amazon.com/images/M/MV5BMjAxMjg5ODI4N15BMl5BanBnXkFtZTYwNjM5Mzg5._V1_SX300.jpg",
        "Ratings": [
            {"Source": "Internet Movie Database", "Value": "8.7/10"},
            {"Source": "Rotten Tomatoes", "Value": "88%"},
            {"Source": "Metacritic", "Value": "73/100"},
        ],
        "Metascore": "73",
        "imdbRating": "8.7",
        "imdbVotes": "1,719,757",
        "imdbID": "tt0133093",
        "Type": "movie",
        "DVD": "21 Sep 1999",
        "BoxOffice": "$171,479,930",
        "Production": "Village Roadshow Prod., Silver Pictures",
        "Website": "N/A",
        "Response": "True",
    }
    result = get_movie_data("tt0133093")
    assert result["Title"] == "The Matrix"
    assert result["Year"] == "1999"
    assert result["Rated"] == "R"
    assert result["Released"] == "31 Mar 1999"
    assert result["Runtime"] == "136 min"
    assert result["Genre"] == "Action, Sci-Fi"
    assert result["Director"] == "Lana Wachowski, Lilly Wachowski"
    assert result["Writer"] == "Lilly Wachowski, Lana Wachowski"
    assert result["Actors"] == "Keanu Reeves, Laurence Fishburne, " \
                                "Carrie-Anne Moss, Hugo Weaving"
    assert result["Plot"] == "A computer hacker learns from mysterious " \
                             "rebels about the true nature of his reality " \
                             "and his role in the war against its controllers."
    assert result["Language"] == "English"
    assert result["Country"] == "USA"
    assert result["Awards"] == "Won 4 Oscars. Another 37 wins & 51 nominations."
    assert result["Poster"] == "https://m.media-amazon.com/images/M/MV5BMjAxMjg5ODI4N15BMl5BanBnXkFtZTYwNjM5Mzg5._V1_SX300.jpg"
    assert result["Ratings"] == [
        {"Source": "Internet Movie Database", "Value": "8.7/10"},
        {"Source": "Rotten Tomatoes", "Value": "88%"},
        {"Source": "Metacritic", "Value": "73/100"},
    ]
    assert result["Metascore"] == "73"
    assert result["imdbRating"] == "8.7"
    assert result["imdbVotes"] == "1,719,757"
    assert result["imdbID"] == "tt0133093"
    assert result["Type"] == "movie"
    assert result["DVD"] == "21 Sep 1999"
    assert result["BoxOffice"] == "$171,479,930"
    assert result["Production"] == "Village Roadshow Prod., Silver Pictures"
    assert result["Website"] == "N/A"
    assert result["Response"] == "True"


@patch('sheepy.core.requests.get')
def test_get_movie_data_http_error(mock_get):
    mock_get.side_effect = requests.exceptions.HTTPError()
    with pytest.raises(SystemExit):
        get_movie_data("tt0133093")


@patch('sheepy.core.requests.get')
def test_get_movie_data_request_exception(mock_get):
    mock_get.side_effect = requests.exceptions.RequestException()
    with pytest.raises(SystemExit):
        get_movie_data("tt0133093")


# @patch('sheepy.core.requests.get')
# def test_get_movie_data_no_response(mock_get):
#     mock_get.return_value = None
#     with pytest.raises(SystemExit):
#         get_movie_data("tt0133093")
