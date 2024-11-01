from dataclasses import dataclass
from typing import Any, Self

from sheepy.model.rating import Rating
from sheepy.util.logger import get_logger


@dataclass
class Movie:
    """
    Represents movie from OMDb API.
    Only relevant fields are saved.
    """

    _logger = get_logger(__name__)

    watched: str
    title: str
    year: str
    genre: str
    runtime: str
    suggested_by: str
    rating: Rating
    director: str
    plot: str
    poster: str

    def __repr__(self) -> str:
        return f"{self.title} ({self.year})"

    def __str__(self) -> str:
        return f"{self.title} ({self.year})"

    def __eq__(self, value: Self) -> bool:
        return (
            self.title == value.title
            and self.year == value.year
            and self.runtime == value.runtime
            and self.director == value.director
        )

    def build_dict(self) -> dict[str, Any]:
        """Build dictionary of class attributes used to display
          or write movie information

        Returns:
            dict[str, Any]: Returns dictionary containing class attributes
        """
        mov_dict: dict[str, Any] = {}
        attr_list = list(self.__dict__.items())
        for field in attr_list:
            if field[0] == "rating":
                imdb = field[1].imdb_rating
                rotten = field[1].tomatometer
                mov_dict["imdb_rating"] = imdb
                mov_dict["tomatometer"] = rotten
                continue
            mov_dict[field[0]] = field[1]
        return mov_dict
