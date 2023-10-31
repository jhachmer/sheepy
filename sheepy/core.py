"""This module contains the core functionality of the sheepy application."""

import argparse
import logging
import os
import sys

import requests

URL = "http://www.omdbapi.com/?apikey="
_API_KEY = os.environ["OMDB_API_KEY"]
SPREADSHEET_ID = os.environ["SPREADSHEET_ID"]
LOG_FORMAT = "[%(asctime)s] {%(filename)s:%(lineno)d} %(levelname)s - %(message)s"

if not os.path.exists("logs/tmp.log"):
    os.mkdir("logs")
    open("logs/tmp.log", "w").close()


logging.basicConfig(
    level=logging.INFO,
    format=LOG_FORMAT,
    handlers=[
        logging.FileHandler(filename="logs/tmp.log"),
        logging.StreamHandler(stream=sys.stdout),
    ],
)

logger = logging.getLogger("sheepy")


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
        help="Set to add to database (This or -v/--view is required)",
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
    """
    Get movie data from the Open Movie Database (OMDb) API.

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
        response = requests.get(URL + _API_KEY + "&i=" + imdb_id)
        response.raise_for_status()
    except requests.exceptions.HTTPError as he:
        logger.error(he)
        raise SystemExit(he)
    except requests.exceptions.RequestException as re:
        logger.error(re)
        raise SystemExit(re)
    except Exception as e:
        logger.error(e)
        raise SystemExit(e)
    response = response.json()
    if response["Response"] == "False":
        logger.error(response["Error"] + " Invalid IMDb ID. Please try again.")
        logger.debug("Used ID: " + imdb_id)
        raise SystemExit(response["Error"] + " Invalid IMDb ID. Please try again.")
    return response


def _get_api_key() -> str:
    """Get the API key for the Open Movie Database (OMDb).

    This function retrieves the API key for the
      Open Movie Database (OMDb) from the environment variables.

    Returns:
        str: The API key for the Open Movie Database (OMDb).
    """
    return os.environ["OMDB_API_KEY"]


if __name__ == "__main__":
    logger.info(get_movie_data("tt0133093"))
