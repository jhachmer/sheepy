import pytest

from sheepy.util import string_util


@pytest.fixture
def test_string():
    return "Hel\nlo \nWor\nld"


@pytest.fixture
def test_url_id():
    return "http://www.omdbapi.com/?apikey=abc123&i=tt1231234"


@pytest.fixture
def test_url_name_year():
    return "http://www.omdbapi.com/?apikey=abc123&t=Test Movie 2&y=1992"


class TestUtil:
    base_url: str = "http://www.omdbapi.com/?apikey="
    fake_api_key: str = "abc123"
    imdb_id: str = "tt1231234"
    title: str = "Test Movie 2"
    year: int = 1992

    def test_insert_newlines(self, test_string):
        assert test_string == string_util.insert_newlines("Hello World", 3)

    def test_build_request_url_imdb_id(self, test_url_id):
        assert test_url_id == string_util.build_request_url(
            self.base_url, self.fake_api_key, self.imdb_id
        )

    def test_build_request_url_title_year(self, test_url_name_year):
        assert test_url_name_year == string_util.build_request_url(
            self.base_url, self.fake_api_key, self.title, self.year
        )
