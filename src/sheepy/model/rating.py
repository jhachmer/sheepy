from typing import Any, Self


class Rating:
    """
    Represents Rating for a movie
    Contains IMDb and Rotten Tomatoes Rating
    """

    imdb_rating: str
    tomatometer: str

    def __init__(self, imdb_rating: str, tomatometer: str) -> None:
        self.imdb_rating = imdb_rating
        self.tomatometer = tomatometer

    def __eq__(self, value: Self) -> bool:
        return (self.imdb_rating == value.imdb_rating) and (
            self.tomatometer == value.tomatometer
        )

    def __repr__(self) -> str:
        return (
            f"""IMDb Rating: {self.imdb_rating} | Rotten Rating: {self.tomatometer}"""
        )

    def __str__(self) -> str:
        return f"""IMDb: {self.imdb_rating}\nRotten: {self.tomatometer}"""

    @classmethod
    def from_json(cls, movie_data: dict[Any, Any]) -> Self:
        """Extracts Ratings from movie dict and returns Rating boject

        Args:
            movie_data (dict[Any, Any]): Dictionary with movie info

        Returns:
            Self: Returns Rating instance with IMDb and RottenTomatoes ratings
        """
        imdb = movie_data.get("imdbRating", "N/A")
        rotten = Rating.extract_tomatometer(movie_data.get("Ratings", []))
        movie_rating = cls(imdb, rotten)
        return movie_rating

    @staticmethod
    def extract_tomatometer(ratings: list[Any] | str) -> str:
        """Extracts Rotten Tomato Rating from movie data dictionary.

        Args:
            ratings (list): List of Ratings from OMDb API

        Returns:
            str: Rotten Tomato Rating in Percentage
        """
        for rating in ratings:
            if rating["Source"] == "Rotten Tomatoes":  # type: ignore
                return rating["Value"]  # type: ignore
        return "N/A"
