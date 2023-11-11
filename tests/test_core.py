# flake8: noqa
import os
from unittest.mock import MagicMock, patch

import ezsheets
import pytest
import requests

from sheepy.core import (
    add_to_sheet,
    extract_movie_data,
    find_free_row,
    find_movie_sheet,
    get_movie_data,
    get_spreadsheet_and_sheet,
    read_user_cli_args,
)

SUGGESTED_BY = os.environ.get("SUGGESTED_BY", "Someone")


@pytest.fixture
def imdb_id():
    return "tt1375666"


@pytest.fixture
def movie_data():
    return {
        "Title": "Inception",
        "Year": "2010",
        "Rated": "PG-13",
        "Released": "16 Jul 2010",
        "Runtime": "148 min",
        "Genre": "Action, Adventure, Sci-Fi",
        "Director": "Christopher Nolan",
        "Writer": "Christopher Nolan",
        "Actors": "Leonardo DiCaprio, Joseph Gordon-Levitt, Ellen Page, Tom Hardy",
        "Plot": "A thief who steals corporate secrets through the use of dream-sharing technology is given the inverse task of planting an idea into the mind of a C.E.O.",
        "Language": "English, Japanese, French",
        "Country": "USA, UK",
        "Awards": "Won 4 Oscars. Another 152 wins & 218 nominations.",
        "Poster": "https://m.media-amazon.com/images/M/MV5BMjAxMjA5MjgxNF5BMl5BanBnXkFtZTcwMjQyMjIyMw@@._V1_SX300.jpg",
        "Ratings": [
            {"Source": "Internet Movie Database", "Value": "8.8/10"},
            {"Source": "Rotten Tomatoes", "Value": "87%"},
            {"Source": "Metacritic", "Value": "74/100"},
        ],
        "Metascore": "74",
        "imdbRating": "8.8",
        "imdbVotes": "2,097,177",
        "imdbID": "tt1375666",
        "Type": "movie",
        "DVD": "07 Dec 2010",
        "BoxOffice": "$292,576,195",
        "Production": "Syncopy, Warner Bros.",
        "Website": "N/A",
        "Response": "True",
    }


@pytest.fixture
def sheet():
    return MagicMock(spec=ezsheets.Sheet)


@pytest.fixture
def ss():
    return MagicMock(spec=ezsheets.Spreadsheet)


def test_read_user_cli_args_add():
    with patch(
        "argparse.ArgumentParser.parse_args",
        return_value=MagicMock(add=True, view=False),
    ):
        args = read_user_cli_args()
        assert args.add is True
        assert args.view is False


def test_read_user_cli_args_view():
    with patch(
        "argparse.ArgumentParser.parse_args",
        return_value=MagicMock(view=True, add=False),
    ):
        args = read_user_cli_args()
        assert args.add is False
        assert args.view is True


def test_get_movie_data(imdb_id, movie_data):
    with patch("requests.get", return_value=MagicMock(json=lambda: movie_data)):
        assert get_movie_data(imdb_id) == movie_data


def test_get_movie_data_http_error(imdb_id):
    with patch("requests.get", side_effect=requests.exceptions.HTTPError):
        with pytest.raises(SystemExit):
            get_movie_data(imdb_id)


def test_get_movie_data_request_exception(imdb_id):
    with patch("requests.get", side_effect=requests.exceptions.RequestException):
        with pytest.raises(SystemExit):
            get_movie_data(imdb_id)


def test_get_movie_data_general_error(imdb_id):
    with patch("requests.get", side_effect=Exception):
        with pytest.raises(SystemExit):
            get_movie_data(imdb_id)


def test_get_movie_data_invalid_id(imdb_id):
    with patch(
        "requests.get",
        return_value=MagicMock(json=lambda: {"Response": "False", "Error": "Error"}),
    ):
        with pytest.raises(SystemExit):
            get_movie_data(imdb_id)


def test_find_movie_sheet():
    spreadsheet = MagicMock(spec=ezsheets.Spreadsheet)
    sheet = MagicMock(title="Sheepy")
    spreadsheet.sheets = [sheet, MagicMock(title="Other")]
    assert find_movie_sheet(spreadsheet) == sheet


def test_find_movie_sheet_not_found():
    spreadsheet = MagicMock(spec=ezsheets.Spreadsheet)
    spreadsheet.sheets = [MagicMock(title="Other"), MagicMock(title="Another")]
    assert find_movie_sheet(spreadsheet) is None


def test_find_free_row():
    sheet = MagicMock(spec=ezsheets.Sheet)
    assert find_free_row(sheet) == sheet.rowCount + 1


def test_extract_movie_data(movie_data):
    extracted_data = extract_movie_data(movie_data, watched=True, add=True)
    assert extracted_data["Watched?"] == "TRUE"
    assert extracted_data["Title"] == "Inception"
    assert extracted_data["Year"] == "2010"
    assert extracted_data["Genre"] == "Action, Adventure, Sci-Fi"
    assert extracted_data["Runtime"] == "148 min"
    assert extracted_data["Suggested by"] == SUGGESTED_BY
    assert extracted_data["IMDb-Rating"] == "8.8"
    assert extracted_data["Tomatometer"] == "87%"
    assert extracted_data["Dirctor"] == "Christopher Nolan"
    assert (
        extracted_data["Plot"]
        == "A thief who steals corporate secrets through the use of dream-sharing technology is given the inverse task of planting an idea into the mind of a C.E.O."
    )
    assert (
        extracted_data["Poster"]
        == '=IMAGE("https://m.media-amazon.com/images/M/MV5BMjAxMjA5MjgxNF5BMl5BanBnXkFtZTcwMjQyMjIyMw@@._V1_SX300.jpg")'
    )
