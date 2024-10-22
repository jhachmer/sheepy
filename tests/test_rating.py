import pytest

from sheepy.model.rating import Rating


@pytest.fixture
def test_rating() -> Rating:
    return Rating("4.5", "45%")


@pytest.fixture
def build_dict_valid_ratings() -> dict:
    mov_dict = {}
    mov_dict["imdb_rating"] = "4.5"
    mov_dict["tomatometer"] = "45%"
    return mov_dict


class TestRating:
    def test_str(self, test_rating):
        assert str(test_rating) == """IMDb: 4.5\nRotten: 45%"""

    def test_repr(self, test_rating):
        assert repr(test_rating) == """IMDb Rating: 4.5 | Rotten Rating: 45%"""

    def test_from_json(self, build_dict_valid_ratings):
        rating = Rating("4.5", "45%")
