"""This module contains the functionality to interact with the OMDb database/API."""

import os
from typing import Any

import requests
from tabulate import tabulate

from sheepy.model.movie import Movie
from sheepy.model.rating import Rating
from sheepy.util.exceptions import MovieRetrievalError
from sheepy.util.logger import get_logger
from sheepy.util.string_util import build_request_url, insert_newlines

omdb_logger = get_logger(__name__)

URL = "http://www.omdbapi.com/?apikey="
API_KEY = os.environ.get("OMDB_API_KEY", "")
if API_KEY == "":
    raise SystemExit(f"Error: API_KEY is not set. {API_KEY}")
SUGGESTED_BY = os.environ.get("SUGGESTED_BY", "Someone")


def _get_movie_data(imdb_id: str) -> dict[str, str]:
    """Get movie data from the Open Movie Database (OMDb) API.
    Uses IMDb-ID for search.

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
        request_url: str = build_request_url(
            base_url=URL, api_key=API_KEY, title_or_id=imdb_id
        )
        response: requests.Response = requests.get(request_url, timeout=60)
        omdb_logger.debug(f"Used request URL: {request_url}")
        response.raise_for_status()
        response_json: dict[str, str] = response.json()
    except requests.exceptions.HTTPError as he:
        omdb_logger.error(f"HTTP Error Code: - {he}")
        raise SystemExit(f"HTTP Error Code: - {str(he)}") from he
    except requests.exceptions.RequestException as re:
        omdb_logger.error(f"Request Error: {re}")
        raise SystemExit(f"Request Error: {str(re)}") from re
    except Exception as e:
        omdb_logger.error(f"General Error: {e}")
        raise SystemExit(f"General Error: {str(e)}") from e

    if response_json["Response"] == "False":
        omdb_logger.error(
            f"{response_json["Error"]} - Invalid IMDb ID: {imdb_id}. Please try again.",
        )
        omdb_logger.debug(f"Used ID: {imdb_id}")
        raise MovieRetrievalError(f"{response_json['Error']} - Invalid IMDb ID.")

    omdb_logger.info(
        f"Successfully retrieved movie data for {response_json["Title"]}"
        f"with IMDb-ID {response_json["imdbID"]}."
    )

    return response_json


def _get_movie_data_by_name_and_year(name: str, year: int) -> dict[str, str]:
    """Get movie data from the Open Movie Database (OMDb) API.
    Uses movie name and release year for search

    Args:
        name (str): Name of movie
        year (int): release year of movie

    Returns:
        dict: A dictionary containing the movie data.

    Raises:
        SystemExit: If an HTTP error occurs.
        SystemExit: If a general request exception occurs.
        ValueError: If no response is received from the API.
    """
    try:
        request_url: str = build_request_url(
            base_url=URL, api_key=API_KEY, title_or_id=name, year=year
        )
        response: requests.Response = requests.get(request_url, timeout=60)
        omdb_logger.debug(f"Used request URL: {request_url}")
        response.raise_for_status()
        response_json: dict[str, str] = response.json()
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
            f"""{response_json["Error"]} - Invalid Movie Name/Year: {name} ({year}).
             Please try again."""
        )
        omdb_logger.debug(f"Used Name and Year: {name} ({year})")
        raise MovieRetrievalError(f"{response_json['Error']} - Invalid IMDb ID.")
    omdb_logger.info(
        "Successfully retrieved movie data for %s with IMDb-ID %s.",
        response_json["Title"],
        response_json["imdbID"],
    )

    return response_json


def show_info(movie_data: dict[str, Any]) -> str:
    """Show the movie information in the CLI.

    Args:
        movie_data (dict): A dictionary containing the movie information.
    """
    try:
        del movie_data["watched"]
        del movie_data["poster"]
        del movie_data["plot"]
    except KeyError:
        omdb_logger.error("Unable to delete keys from movie dict")
    table: list[list[str]] = [list(movie_data.keys()), list(movie_data.values())]
    return tabulate(
        table,
        headers="firstrow",
        tablefmt="plain",
        stralign="center",
        numalign="center",
    )


def _extract_movie_data(
    movie_data: dict[str, str],
    watched: bool,
    add: bool,
    suggested_by: str = SUGGESTED_BY,
) -> Movie:
    """Extract only the necessary data from the movie_data dictionary.

    Args:
        movie_data (dict): The movie data received from OMDb.
        watched (bool): Set to true to check watched-checkbox.
        add (bool): Set to true when adding to spreadsheet

    Returns:
        Movie: The relevant movie data that is added to the sheet
    """
    movie: Movie = Movie(
        watched="TRUE" if watched else "FALSE",
        title=movie_data.get("Title", ""),
        year=movie_data.get("Year", ""),
        genre=movie_data.get("Genre", ""),
        runtime=movie_data.get("Runtime", ""),
        suggested_by=suggested_by,
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
        rating=Rating.from_json(movie_data),
    )
    return movie


def process_movie_request_imdb_id(
    imdb_id: str,
    watched: bool = False,
    add: bool = True,
    suggested_by: str = SUGGESTED_BY,
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
    try:
        raw_movie_info: dict[str, str] = _get_movie_data(imdb_id)
    except MovieRetrievalError as mre:
        mre.add_note(f"Error processing movie request with ID: {imdb_id}")
        raise
    extr_movie_data: Movie = _extract_movie_data(
        raw_movie_info, watched, add, suggested_by
    )
    movie_dict = extr_movie_data.build_dict()
    return movie_dict


def process_movie_request_name_year(
    name: str,
    year: int,
    watched: bool = False,
    add: bool = True,
    suggested_by: str = SUGGESTED_BY,
) -> dict[str, str]:
    """
    Processes movie request from OMDb API and creates dict with movie data

    Args:
        name (str): Name of movie
        year (int): release year of movie
        watched (bool, optional): Whether to tick watched?-checkbox. Defaults to False
        add (bool, optional): Whether to add movie data. Defaults to True

    Returns:
        dict: Dictionary containing movie data
    """
    try:
        raw_movie_info: dict[str, str] = _get_movie_data_by_name_and_year(name, year)
    except MovieRetrievalError as mre:
        mre.add_note(
            f"Error processing movie request with name and year: {name} ({year})"
        )
        raise
    extr_movie_data: Movie = _extract_movie_data(
        raw_movie_info, watched, add, suggested_by
    )
    movie_dict = extr_movie_data.build_dict()
    return movie_dict
