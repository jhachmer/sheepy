"""This module contains the core functionality of the sheepy application."""

import argparse
import os

import requests
from dotenv import load_dotenv
from requests import Response
from tabulate import tabulate

from sheepy.util.logger import get_logger
from sheepy.util.util import insert_newlines

load_dotenv()

URL = "http://www.omdbapi.com/?apikey="
API_KEY = os.environ.get("OMDB_API_KEY")

if API_KEY is None:
    raise SystemExit(f"API_KEY is not set. {API_KEY}")

SUGGESTED_BY = os.environ.get("SUGGESTED_BY", "Someone")
TEST = True if os.environ.get("TEST", "False") == "True" else False
SPREADSHEET_ID = (
    os.environ.get("SPREADSHEET_ID", "")
    if not TEST
    else os.environ.get("SPREADSHEET_ID_TEST", "")
)

omdb_logger = get_logger(__name__)

COLUMNS = [
    "Watched?",
    "Title",
    "Year",
    "Genre",
    "Runtime",
    "Suggested by",
    "IMDb Score",
    "Tomatometer",
    "Director",
    "Plot",
    "Movie Poster",
]


def read_user_cli_args() -> argparse.Namespace:
    """Handles the CLI user interactions.

    Returns:
        argparse.Namespace: Populated namespace object
    """
    parser = argparse.ArgumentParser(
        description="Add or view movies to your personal database."
    )
    parser.add_argument("imdb_id", nargs=1, type=str, help="Enter the movies imdb id.")
    mut_req_group = parser.add_mutually_exclusive_group(required=True)
    mut_req_group.add_argument(
        "-a",
        "--add",
        action="store_true",
        help="Set to add to sheet (This or -v/--view is required)",
    )
    mut_req_group.add_argument(
        "-v",
        "--view",
        action="store_true",
        help="Set to view in the CLI (This or -a/--add is required)",
    )
    parser.add_argument(
        "-w",
        "--watched",
        action="store_true",
        help="Set to mark movie as already watched (Defaults to False)",
    )

    return parser.parse_args()


def get_movie_data(imdb_id: str) -> dict:
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


def extract_movie_data(movie_data: dict, watched: bool, add: bool) -> dict:
    """Extract only the necessary data from the movie_data dictionary.

    Args:
        movie_data (dict): The movie data to extract from.
        watched (bool): Set to true to check watched-checkbox.
        add (bool): Set to true when adding to spreadsheet

    Returns:
        dict: A new dictionary with only the necessary data.
    """
    extracted_data: dict[str, str] = {}
    extracted_data["Watched?"] = "TRUE" if watched else "FALSE"
    extracted_data["Title"] = movie_data.get("Title", "")
    extracted_data["Year"] = movie_data.get("Year", "")
    extracted_data["Genre"] = movie_data.get("Genre", "")
    extracted_data["Runtime"] = movie_data.get("Runtime", "")
    extracted_data["Suggested by"] = SUGGESTED_BY
    extracted_data["IMDb-Rating"] = movie_data.get("imdbRating", "N/A")
    extracted_data["Tomatometer"] = next(
        (
            rating["Value"]
            for rating in movie_data.get("Ratings", [])
            if rating["Source"] == "Rotten Tomatoes"
        ),
        "N/A",
    )
    extracted_data["Dirctor"] = movie_data.get("Director", "")
    extracted_data["Plot"] = (
        movie_data.get("Plot", "")
        if add
        else insert_newlines(movie_data.get("Plot", ""), 30)
    )
    extracted_data["Poster"] = (
        f"=IMAGE(\"{movie_data.get('Poster')}\")"
        if add
        else insert_newlines(movie_data.get("Poster", ""), 30)
    )

    return extracted_data
