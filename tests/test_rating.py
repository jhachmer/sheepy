import pytest

from sheepy.model.rating import Rating


@pytest.fixture
def test_rating() -> Rating:
    return Rating("4.5", "45%")


@pytest.fixture
def raw_movie_info() -> dict[str, str | list[dict[str, str]]]:
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


class TestRating:
    def test_str(self, test_rating):
        assert str(test_rating) == """IMDb: 4.5\nRotten: 45%"""

    def test_repr(self, test_rating):
        assert repr(test_rating) == """IMDb Rating: 4.5 | Rotten Rating: 45%"""

    def test_from_json(self, raw_movie_info):
        expected_rating = Rating("8.1", "89%")
        json_rating = Rating.from_json(raw_movie_info)
        assert json_rating == expected_rating
