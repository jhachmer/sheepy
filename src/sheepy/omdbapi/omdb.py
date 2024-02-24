"""This module contains the core functionality of the sheepy application."""

import os
from dataclasses import asdict, dataclass
from typing import Any

import requests
from dotenv import load_dotenv
from requests import Response
from tabulate import tabulate

from sheepy.util.logger import get_logger
from sheepy.util.string_util import insert_newlines

load_dotenv()

URL = "http://www.omdbapi.com/?apikey="
API_KEY = os.environ.get("OMDB_API_KEY", "")
if API_KEY == "":
    raise SystemExit(f"Error: API_KEY is not set. {API_KEY}")
SUGGESTED_BY = os.environ.get("SUGGESTED_BY", "Someone")
SPREADSHEET_ID = os.environ.get("SPREADSHEET_ID", "")

omdb_logger = get_logger(__name__)


@dataclass
class Movie:
    """Represents movie from OMDb API."""

    watched: str
    title: str
    year: str
    genre: str
    runtime: str
    suggested_by: str
    imdb_rating: str
    tomatometer: str
    director: str
    plot: str
    poster: str


def _get_movie_data(imdb_id: str) -> dict:
    """Get movie data from the Open Movie Database (OMDb) API.

    Args:
        imdb_id (str): The IMDb ID of the movie to search for.

    Returns:
        dict: A dictionary containing the movie data.

    Raises:
        SystemExit: If an HTTP error occurs.
        SystemExit: If a general request exception occurs.
        ValueError: If no response is received from the API.
    """
    try:
        response: Response = requests.get(URL + API_KEY + "&i=" + imdb_id, timeout=60)
        response.raise_for_status()
        response_json: dict = response.json()
    except requests.exceptions.HTTPError as he:
        omdb_logger.error("HTTP Error Code: - %s", str(he))
        raise SystemExit(f"HTTP Error Code: - {str(he)}") from he
    except requests.exceptions.RequestException as re:
        omdb_logger.error("Request Error: %s", str(re))
        raise SystemExit(f"Request Error: {str(re)}") from re
    except Exception as e:
        omdb_logger.error("General Error: %s", str(e))
        raise SystemExit(f"General Error: {str(e)}") from e

    if response_json["Response"] == "False":
        omdb_logger.error(
            "%s - Invalid IMDb ID: %s. Please try again.",
            response_json["Error"],
            imdb_id,
        )
        omdb_logger.debug("Used ID: %s", imdb_id)
        raise SystemExit(f"{response_json['Error']} - Invalid IMDb ID.")

    omdb_logger.info(
        "Successfully retrieved movie data for %s.", response_json["Title"]
    )

    return response_json


def show_info(movie_data: dict) -> None:
    """Show the movie information in the CLI.

    Args:
        movie_data (dict): A dictionary containing the movie information.
    """
    table = [list(movie_data.keys()), list(movie_data.values())]
    print(
        tabulate(
            table,
            headers="firstrow",
            tablefmt="fancy_grid",
            stralign="center",
            numalign="center",
        )
    )


def _extract_movie_data(
    movie_data: dict[str, Any], watched: bool, add: bool
) -> dict[str, str]:
    """Extract only the necessary data from the movie_data dictionary.

    Args:
        movie_data (dict): The movie data to extract from.
        watched (bool): Set to true to check watched-checkbox.
        add (bool): Set to true when adding to spreadsheet

    Returns:
        dict: A new dictionary with only the necessary data.
    """
    movie: Movie = Movie(
        watched="TRUE" if watched else "FALSE",
        title=movie_data.get("Title", ""),
        year=movie_data.get("Year", ""),
        genre=movie_data.get("Genre", ""),
        runtime=movie_data.get("Runtime", ""),
        suggested_by=SUGGESTED_BY,
        imdb_rating=movie_data.get("imdbRating", "N/A"),
        tomatometer=_extract_tomatometer(movie_data.get("Ratings", [])),
        director=movie_data.get("Director", ""),
        plot=(
            movie_data.get("Plot", "")
            if add
            else insert_newlines(movie_data.get("Plot", ""), 30)
        ),
        poster=(
            f"=IMAGE(\"{movie_data.get('Poster')}\")"
            if add
            else insert_newlines(movie_data.get("Poster", ""), 30)
        ),
    )
    return asdict(movie)


def _extract_tomatometer(ratings: list) -> str:
    """Extracts Rotten Tomato Rating from movie data dictionary.

    Args:
        ratings (list): List of Ratings from OMDb API

    Returns:
        str: Rotten Tomato Rating in Percentage
    """
    tomato_rating: str = next(
        (
            rating["Value"]
            for rating in ratings
            if rating["Source"] == "Rotten Tomatoes"
        ),
        "N/A",
    )
    return tomato_rating


def process_movie_request(
    imdb_id: str, watched: bool = False, add: bool = True
) -> dict[str, str]:
    """
    Processes movie request from OMDb API and creates dict with movie data

    Args:
        imdb_id (str): IMDB ID
        watched (bool, optional): Whether to tick watched?-checkbox. Defaults to False
        add (bool, optional): Whether to add movie data. Defaults to True

    Returns:
        dict: Dictionary containing movie data
    """
    movie_info: dict = _get_movie_data(imdb_id)
    return _extract_movie_data(movie_info, watched, add)
