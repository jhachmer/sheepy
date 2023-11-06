"""This module contains the core functionality of the sheepy application."""

import argparse
import logging
import os
import sys

import ezsheets
import requests
from tabulate import tabulate

LOG_FORMAT = "[%(asctime)s] {%(filename)s:%(lineno)d} %(levelname)s - %(message)s"

logging.basicConfig(
    level=logging.DEBUG,
    format=LOG_FORMAT,
    handlers=[
        logging.FileHandler(filename="logs/tmp.log"),
        logging.StreamHandler(stream=sys.stdout),
    ],
)

logger = logging.getLogger("sheepy")


URL = "http://www.omdbapi.com/?apikey="
API_KEY = os.environ.get("OMDB_API_KEY")
TEST = True if os.environ.get("TEST") == "True" else False
SPREADSHEET_ID = (
    os.environ.get("SPREADSHEET_ID", "")
    if not TEST
    else os.environ.get("SPREADSHEET_ID_TEST", "")
)


COLUMNS = [
    "Watched?",
    "Title",
    "Year",
    "Genre",
    "Runtime",
    "Suggested by",
    "IMDb Score",
    "Rotten Tomatoes Score",
    "Director",
    "Plot",
    "Movie Poster",
]

if not os.path.exists("logs/tmp.log"):
    os.mkdir("logs")
    open("logs/tmp.log", "w").close()


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
        response = requests.get(URL + API_KEY + "&i=" + imdb_id)
        response.raise_for_status()
    except requests.exceptions.HTTPError as he:
        logger.error("HTTP Error Code: - " + str(he))
        raise SystemExit("HTTP Error Code: - " + str(he))
    except requests.exceptions.RequestException as re:
        logger.error("Request Error: " + str(re))
        raise SystemExit("Request Error: " + str(re))
    except Exception as e:
        logger.error("General Error: " + str(e))
        raise SystemExit("General Error: " + str(e))

    response = response.json()
    if response["Response"] == "False":
        logger.error(response["Error"] + " Invalid IMDb ID. Please try again.")
        logger.debug("Used ID: " + imdb_id)
        raise SystemExit(response["Error"] + " Invalid IMDb ID. Please try again.")

    logger.info("Successfully retrieved movie data for " + response["Title"] + ".")
    return response


def _get_api_key() -> str:
    """Get the API key for the Open Movie Database (OMDb).

    This function retrieves the API key for the
      Open Movie Database (OMDb) from the environment variables.

    Returns:
        str: The API key for the Open Movie Database (OMDb).
    """
    return os.environ["OMDB_API_KEY"]


def _get_spreadsheet_id() -> str:
    """Get the spreadsheet ID for the Google Sheet.

    This function retrieves the spreadsheet ID for the
      Google Sheet from the environment variables.

    Returns:
        str: The spreadsheet ID for the Google Sheet.
    """
    return os.environ["SPREADSHEET_ID"]


def setup_new_sheet(sh_id: str = SPREADSHEET_ID) -> str:
    """Setup a new Google Sheet for the user.

    This function creates a new Google Sheet for the user to use.
    """
    try:
        ss = (
            ezsheets.createSpreadsheet(title="Sheepy Spreadsheet")
            if sh_id == ""
            else ezsheets.Spreadsheet(sh_id)
        )

        sh = ss.createSheet(title="Sheepy", rowCount=1000, columnCount=len(COLUMNS))
        sh.updateRow(1, COLUMNS)
        logger.info(
            "Successfully created spreadsheet: " + ss.title + " with ID: " + ss.id
        )
        logger.info(
            "Successfully created sheet: "
            + sh.title
            + " with "
            + str(sh.rowCount)
            + " rows and "
            + str(sh.columnCount)
            + " columns."
        )
    except ezsheets.EZSheetsException as eze:
        logger.error("Error creating spreadsheet: " + eze)
        raise SystemExit("Error creating spreadsheet: " + eze)
    return (ss, sh)


def find_free_row(sheet: ezsheets.Sheet) -> int:
    """Find the first free row in the spreadsheet.

    This function finds the first free row in the spreadsheet
      and returns it.

    Args:
        sheet (ezsheets.Sheet): The sheet to search for the first free row.

    Returns:
        int: The first free row in the spreadsheet.
    """
    for i in range(1, sheet.rowCount):
        if sheet.get(1, i) == [""]:
            return i
    return sheet.rowCount + 1


def show_info(movie_data: dict) -> None:
    """Show the movie information in the CLI.

    This function shows the movie information in the CLI.

    Args:
        movie_data (dict): The movie data to show.
    """
    table = [COLUMNS, extract_movie_data(movie_data)]
    print(tabulate(table, headers="firstrow", tablefmt="fancy_grid"))


def extract_movie_data(movie_data: dict) -> list:
    """Extract only the necessary data from the movie_data dictionary.

    This function extracts only the necessary data from the movie_data dictionary
    and returns a new list with the extracted data.

    Args:
        movie_data (dict): The movie data to extract from.

    Returns:
        list: A new list with only the necessary data.
    """
    extracted_data = []
    extracted_data.append(movie_data.get("Title", ""))
    extracted_data.append(movie_data.get("Year", ""))
    extracted_data.append(movie_data.get("Genre", ""))
    extracted_data.append(movie_data.get("Runtime", ""))
    extracted_data.append(movie_data.get("imdbRating", ""))
    extracted_data.append(
        next(
            (
                rating["Value"]
                for rating in movie_data.get("Ratings", [])
                if rating["Source"] == "Rotten Tomatoes"
            ),
            "",
        )
    )
    extracted_data.append(movie_data.get("Director", ""))
    # extracted_data.append(movie_data.get("Plot", ""))
    extracted_data.append(
        "Kurzer Text aber bisschen länger\nKurzer Text aber bisschen länger"
    )
    extracted_data.append(movie_data.get("Poster", ""))
    return extracted_data


def add_to_sheet(movie_data: dict, sheet: ezsheets.Sheet) -> None:
    pass


if __name__ == "__main__":
    print("This is the core module.")
    md = get_movie_data("tt0133093")
    show_info(md)
