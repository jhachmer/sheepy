import pytest

from sheepy.model.movie import Movie
from sheepy.model.rating import Rating


@pytest.fixture
def exp_repr() -> str:
    return "Test (1992), Rt:109, W:TRUE"


@pytest.fixture
def exp_str() -> str:
    return "Test (1992)"


@pytest.fixture
def build_dict_valid_ratings() -> dict:
    mov_dict = {}
    mov_dict["watched"] = "TRUE"
    mov_dict["title"] = "Test"
    mov_dict["year"] = "1992"
    mov_dict["genre"] = "Horror, Thriller, Drama"
    mov_dict["runtime"] = "109"
    mov_dict["suggested_by"] = "Jannes"
    mov_dict["imdb_rating"] = "4.5"
    mov_dict["tomatometer"] = "45%"
    mov_dict["director"] = "Somebody"
    mov_dict["plot"] = "Something happens"
    mov_dict["poster"] = "some url"
    return mov_dict


@pytest.fixture
def build_dict_no_ratings() -> dict:
    mov_dict = {}
    mov_dict["watched"] = "TRUE"
    mov_dict["title"] = "Test"
    mov_dict["year"] = "1992"
    mov_dict["genre"] = "Horror, Thriller, Drama"
    mov_dict["runtime"] = "109"
    mov_dict["suggested_by"] = "Jannes"
    mov_dict["imdb_rating"] = "N/A"
    mov_dict["tomatometer"] = "N/A"
    mov_dict["director"] = "Somebody"
    mov_dict["plot"] = "Something happens"
    mov_dict["poster"] = "some url"
    return mov_dict


class TestMovie:
    base = Movie(
        "TRUE",
        "Test",
        "1992",
        "Horror, Thriller, Drama",
        "109",
        "Jannes",
        Rating(),
        "Somebody",
        "Something happens",
        "some url",
    )

    def test_repr(self, exp_repr):
        assert exp_repr == repr(self.base)

    def test_str(self, exp_str):
        assert exp_str == str(self.base)

    def test_build_dict_valid_rating(self, build_dict_valid_ratings):
        mov = self.base
        mov.rating = Rating("4.5", "45%")
        got = mov.build_dict()
        assert build_dict_valid_ratings == got

    def test_build_dict_no_ratings(self, build_dict_no_ratings):
        mov = self.base
        mov.rating = Rating()
        got = mov.build_dict()
        assert build_dict_no_ratings == got
