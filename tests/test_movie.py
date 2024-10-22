import pytest

from sheepy.model.movie import Movie
from sheepy.model.rating import Rating


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
    @pytest.fixture
    def mov(self):
        return Movie(
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

    @pytest.fixture
    def same_movie(self, mov) -> tuple[Movie, Movie]:
        return mov, mov

    @pytest.fixture
    def diff_movie(self, mov) -> tuple[Movie, Movie]:
        other = Movie(
            "TRUE",
            "Not the Same",
            "1992",
            "Horror, Thriller, Drama",
            "109",
            "Jannes",
            Rating(),
            "Somebody",
            "Something happens",
            "some url",
        )
        return mov, other

    def test_mov_repr(self, mov):
        assert "Test (1992)" == repr(mov)

    def test_mov_str(self, mov):
        assert "Test (1992)" == str(mov)

    @pytest.mark.parametrize(
        "got,expected", [("same_movie", True), ("diff_movie", False)]
    )
    def test_mov_eq(self, got, expected, request):
        mov1, mov2 = request.getfixturevalue(got)
        assert (mov1 == mov2) == expected

    def test_build_dict_valid_rating(self, build_dict_valid_ratings, mov):
        mov = mov
        mov.rating = Rating("4.5", "45%")
        got = mov.build_dict()
        assert build_dict_valid_ratings == got

    def test_build_dict_no_ratings(self, build_dict_no_ratings, mov):
        mov = mov
        mov.rating = Rating()
        got = mov.build_dict()
        assert build_dict_no_ratings == got
