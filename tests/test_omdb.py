import pytest
from sheepy.omdbapi.omdb import Movie, _extract_movie_data


@pytest.fixture
def raw_movie_info() -> dict[str, str]:
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


def test_extract_movie_data(raw_movie_info):
    mov = Movie(
        watched="TRUE",
        title="Blade Runner",
        year="1982",
        genre="Action, Drama, Sci-Fi",
        runtime="117 min",
        suggested_by="Jannes",
        imdb_rating="8.1",
        tomatometer="89%",
        director="Ridley Scott",
        plot="A blade runner must pursue and terminate four replicants who stole a ship in space and have returned to Earth to find their creator.",
        poster='=IMAGE("https://m.media-amazon.com/images/M/MV5BNzQzMzJhZTEtOWM4NS00MTdhLTg0YjgtMjM4MDRkZjUwZDBlXkEyXkFqcGdeQXVyNjU0OTQ0OTY@._V1_SX300.jpg")',
    )
    assert mov == _extract_movie_data(raw_movie_info, watched=True, add=True)
