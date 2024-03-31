import pytest
from sheepy.util.string_util import insert_newlines


@pytest.fixture
def test_string():
    return "Hel\nlo \nWor\nld"


def test_insert_newlines(test_string):
    assert test_string == insert_newlines("Hello World", 3)
