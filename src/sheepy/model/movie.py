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
        return f"{self.title} ({self.year}), Rt:{self.runtime}, W:{self.watched}"

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
        """Build dictionary of class attributes used to display movie information

        Returns:
            dict[str, Any]: _description_
        """
        mov_dict: dict[str, Any] = {}
        attr_list = list(self.__dict__.items())
        for field in attr_list:
            if field[0] == "rating":
                try:
                    imdb = field[1].imdb_rating
                    rotten = field[1].tomatometer
                    if imdb is None:
                        mov_dict["imdb_rating"] = "N/A"
                    else:
                        mov_dict["imdb_rating"] = imdb
                    if rotten is None:
                        mov_dict["tomatometer"] = "N/A"
                    else:
                        mov_dict["tomatometer"] = rotten
                    continue
                except AttributeError:
                    self._logger.error("Error retrieving rating data")
                    mov_dict["imdb_rating"] = "N/A"
                    mov_dict["tomatometer"] = "N/A"
            mov_dict[field[0]] = field[1]
        return mov_dict
