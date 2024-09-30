from dataclasses import dataclass
from typing import Any

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
        return f"""{self.title} ({self.year}) {self.runtime} min.
         Suggested by: {self.suggested_by}"""

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
                    mov_dict["imdb_rating"] = field[1].imdb_rating
                    mov_dict["tomatometer"] = field[1].tomatometer
                    continue
                except AttributeError:
                    self._logger.error("Error retrieving rating data")
                    mov_dict["imdb_rating"] = "N/A"
                    mov_dict["tomatometer"] = "N/A"
            mov_dict[field[0]] = field[1]
        return mov_dict
