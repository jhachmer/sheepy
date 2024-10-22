from typing import Any

import pytest
from tabulate import tabulate

from sheepy.model.movie import Movie
from sheepy.model.rating import Rating
from sheepy.omdb import api


@pytest.fixture
def raw_movie_info() -> dict[str, Any]:
    return {
        "Title": "Blade Runner",
        "Year": "1982",
        "Rated": "R",
        "Released": "25 Jun 1982",
        "Runtime": "117 min",
        "Genre": "Action, Drama, Sci-Fi",
        "Director": "Ridley Scott",
        "Writer": "Hampton Fancher, David Webb Peoples, Philip K. Dick",
        "Actors": "Harrison Ford, Rutger Hauer, Sean Young",
        "Plot": "A blade runner must pursue and terminate four replicants who stole a ship in space and have returned to Earth to find their creator.",
        "Language": "English, German, Cantonese, Japanese, Hungarian, Arabic, Korean",
        "Country": "United States, United Kingdom",
        "Awards": "Nominated for 2 Oscars. 13 wins & 22 nominations total",
        "Poster": "https://m.media-amazon.com/images/M/MV5BNzQzMzJhZTEtOWM4NS00MTdhLTg0YjgtMjM4MDRkZjUwZDBlXkEyXkFqcGdeQXVyNjU0OTQ0OTY@._V1_SX300.jpg",
        "Ratings": [
            {"Source": "Internet Movie Database", "Value": "8.1/10"},
            {"Source": "Rotten Tomatoes", "Value": "89%"},
            {"Source": "Metacritic", "Value": "84/100"},
        ],
        "Metascore": "84",
        "imdbRating": "8.1",
        "imdbVotes": "817,983",
        "imdbID": "tt0083658",
        "Type": "movie",
        "DVD": "09 Jun 2013",
        "BoxOffice": "$32,914,489",
        "Production": "N/A",
        "Website": "N/A",
        "Response": "True",
    }


@pytest.fixture
def movie_dict():
    return {
        "watched": "TRUE",
        "title": "Blade Runner",
        "year": "1982",
        "genre": "Action, Drama, Sci-Fi",
        "runtime": "117 min",
        "suggested_by": "Jannes",
        "director": "Ridley Scott",
        "plot": "A blade runner must pursue and terminate four replicants who stole a ship in space and have returned to Earth to find their creator.",
        "poster": '=IMAGE("https://m.media-amazon.com/images/M/MV5BNzQzMzJhZTEtOWM4NS00MTdhLTg0YjgtMjM4MDRkZjUwZDBlXkEyXkFqcGdeQXVyNjU0OTQ0OTY@._V1_SX300.jpg")',
        "tomatometer": "89%",
        "imdb_rating": "8.1",
    }


@pytest.fixture
def movie_data():
    return Movie(
        watched="TRUE",
        title="Blade Runner",
        year="1982",
        genre="Action, Drama, Sci-Fi",
        runtime="117 min",
        suggested_by="Jannes",
        director="Ridley Scott",
        plot="A blade runner must pursue and terminate four replicants who stole a ship in space and have returned to Earth to find their creator.",
        poster='=IMAGE("https://m.media-amazon.com/images/M/MV5BNzQzMzJhZTEtOWM4NS00MTdhLTg0YjgtMjM4MDRkZjUwZDBlXkEyXkFqcGdeQXVyNjU0OTQ0OTY@._V1_SX300.jpg")',
        rating=Rating("8.1", "89%"),
    )


@pytest.fixture
def ratings():
    return [
        {"Source": "Internet Movie Database", "Value": "8.1/10"},
        {"Source": "Rotten Tomatoes", "Value": "89%"},
    ]


@pytest.fixture
def table_list():
    d = {
        "title": "Blade Runner",
        "year": "1982",
        "genre": "Action, Drama, Sci-Fi",
        "runtime": "117 min",
        "suggested_by": "Jannes",
        "director": "Ridley Scott",
        # "plot": "A blade runner must pursue and terminate four replicants who stole a ship in space and have returned to Earth to find their creator.",
        "tomatometer": "89%",
        "imdb_rating": "8.1",
    }
    return [list(d.keys()), list(d.values())]


@pytest.fixture
def mock_data():
    return {
        "Title": "Blade Runner",
        "Year": "1982",
        "Rated": "R",
        "Released": "25 Jun 1982",
        "Runtime": "117 min",
        "Genre": "Action, Drama, Sci-Fi",
        "Director": "Ridley Scott",
        "Writer": "Hampton Fancher, David Webb Peoples, Philip K. Dick",
        "Actors": "Harrison Ford, Rutger Hauer, Sean Young",
        "Plot": "A blade runner must pursue and terminate four replicants who stole a ship in space and have returned to Earth to find their creator.",
        "Language": "English, German, Cantonese, Japanese, Hungarian, Arabic, Korean",
        "Country": "United States, United Kingdom",
        "Awards": "Nominated for 2 Oscars. 13 wins & 22 nominations total",
        "Poster": "https://m.media-amazon.com/images/M/MV5BNzQzMzJhZTEtOWM4NS00MTdhLTg0YjgtMjM4MDRkZjUwZDBlXkEyXkFqcGdeQXVyNjU0OTQ0OTY@._V1_SX300.jpg",
        "Ratings": [
            {"Source": "Internet Movie Database", "Value": "8.1/10"},
            {"Source": "Rotten Tomatoes", "Value": "89%"},
            {"Source": "Metacritic", "Value": "84/100"},
        ],
        "Metascore": "84",
        "imdbRating": "8.1",
        "imdbVotes": "817,983",
        "imdbID": "tt0083658",
        "Type": "movie",
        "DVD": "09 Jun 2013",
        "BoxOffice": "$32,914,489",
        "Production": "N/A",
        "Website": "N/A",
        "Response": "True",
    }


class TestOmdb:
    def test_extract_movie_data(self, raw_movie_info, movie_data):
        assert movie_data == api._extract_movie_data(
            raw_movie_info, watched=True, add=True
        )

    def test_extract_tomatometer(self, ratings):
        assert Rating.extract_tomatometer(ratings) == "89%"

    def test_get_movie_data_by_name_and_year(self, mocker, mock_data):
        mocker.patch(
            "sheepy.omdb.api._get_movie_data_by_name_and_year", return_value=mock_data
        )

        result = api._get_movie_data_by_name_and_year("Blade Runner", 1982)

        assert result == mock_data
        assert type(result) is dict
        assert result["Title"] == "Blade Runner"

    def test_get_movie_data(self, mocker, mock_data):
        mocker.patch("sheepy.omdb.api._get_movie_data", return_value=mock_data)

        result = api._get_movie_data("tt0083658")

        assert result == mock_data
        assert type(result) is dict
        assert result["Title"] == "Blade Runner"

    def test_process_movie_request_imdb_id(self, mocker, movie_dict, mock_data):
        mocker.patch("sheepy.omdb.api._get_movie_data", return_value=mock_data)

        result = api.process_movie_request_imdb_id("tt0083658", watched=True, add=True)
        expected = movie_dict

        assert result == expected

    def test_process_movie_request_name_year(self, mocker, movie_dict, mock_data):
        mocker.patch(
            "sheepy.omdb.api._get_movie_data_by_name_and_year", return_value=mock_data
        )

        result = api.process_movie_request_name_year(
            "Blade Runner", 1982, watched=True, add=True
        )
        expected = movie_dict

        assert result == expected

    def test_show_info(self, table_list, movie_dict):
        assert tabulate(
            table_list,
            headers="firstrow",
            tablefmt="plain",
            stralign="center",
            numalign="center",
        ) == api.show_info(movie_dict)
