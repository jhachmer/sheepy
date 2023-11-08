"""This module contains the core functionality of the sheepy application."""

import argparse
import logging
import os
import sys

import ezsheets
import requests
from tabulate import tabulate
from util import insert_newlines


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
SUGGESTED_BY = os.environ.get("SUGGESTED_BY", "Someone")
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
    "Tomatometer",
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
        logger.error(f"HTTP Error Code: - {str(he)}")
        raise SystemExit(f"HTTP Error Code: - {str(he)}")
    except requests.exceptions.RequestException as re:
        logger.error(f"Request Error: {str(re)}")
        raise SystemExit(f"Request Error: {str(re)}")
    except Exception as e:
        logger.error(f"General Error: {str(e)}")
        raise SystemExit(f"General Error: {str(e)}")

    response = response.json()
    if response["Response"] == "False":
        logger.error(f"{response['Error']} - Invalid IMDb ID. Please try again.")
        logger.debug(f"Used ID: {imdb_id}")
        raise SystemExit(f"{response['Error']} - Invalid IMDb ID. Please try again.")

    logger.info(f"Successfully retrieved movie data for {response['Title']}.")

    return response


def get_spreadsheet_and_sheet(sh_id: str = SPREADSHEET_ID) -> str:
    """Setup a new Google Sheet for the user.

    This function creates a new Google Sheet for the user to use.
    """
    try:
        ss = (
            ezsheets.createSpreadsheet(title="Sheepy Spreadsheet")
            if sh_id == ""
            else ezsheets.Spreadsheet(sh_id)
        )
        logger.info(f"Found spreadsheet: {ss.title} with ID: {ss.id}")

        sh = find_movie_sheet(ss)
        if sh is None:
            logger.info("No sheet named 'Sheepy' found. Creating new sheet.")
            sh = ss.createSheet(title="Sheepy", rowCount=1000, columnCount=len(COLUMNS))
            sh.updateRow(1, COLUMNS)
            logger.info(
                f"Successfully created sheet: {sh.title} with {str(sh.rowCount)}"
                f"rows and {str(sh.columnCount)} columns."
            )

    except ezsheets.EZSheetsException as eze:
        logger.error(f"Error creating spreadsheet: {eze}")
        raise SystemExit("Error creating spreadsheet: " + eze)

    return (ss, sh)


def find_movie_sheet(spreadsheet: ezsheets.Spreadsheet) -> ezsheets.Sheet:
    """
    Finds and returns the sheet named 'Sheepy' in the given spreadsheet.

    Args:
        spreadsheet (ezsheets.Spreadsheet): The spreadsheet to search for the sheet.

    Returns:
        ezsheets.Sheet: The sheet named 'Sheepy', or None if it is not found.
    """
    for sheet in spreadsheet.sheets:
        if sheet.title == "Sheepy":
            return sheet

    return None


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
        if sheet.get(2, i) == "":
            return i

    return sheet.rowCount + 1


def show_info(movie_data: dict) -> None:
    """
    Show the movie information in the CLI.

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
    """
    Extract only the necessary data from the movie_data dictionary.

    This function extracts only the necessary data from the movie_data dictionary
    and returns a new dictionary with the extracted data.

    Args:
        movie_data (dict): The movie data to extract from.

    Returns:
        dict: A new dictionary with only the necessary data.
    """
    extracted_data = {}
    extracted_data["Watched?"] = "TRUE" if watched else "FALSE"
    extracted_data["Title"] = movie_data.get("Title", "")
    extracted_data["Year"] = movie_data.get("Year", "")
    extracted_data["Genre"] = movie_data.get("Genre", "")
    extracted_data["Runtime"] = movie_data.get("Runtime", "")
    extracted_data["Suggested by"] = SUGGESTED_BY
    extracted_data["IMDb-Rating"] = movie_data.get("imdbRating", "")
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
        movie_data.get("Plot")
        if add
        else insert_newlines(movie_data.get("Plot", ""), 30)
    )
    extracted_data["Poster"] = (
        f"=IMAGE(\"{movie_data.get('Poster')}\")"
        if add
        else insert_newlines(movie_data.get("Poster", ""), 30)
    )

    return extracted_data


def add_to_sheet(movie_data: dict, sheet: ezsheets.Sheet) -> None:
    """
    Adds a movie's data to the specified Google Sheet.

    Args:
        movie_data (dict): A dictionary containing the movie's data.
        sheet (ezsheets.Sheet): The Google Sheet to add the movie's data to.
    """
    row = find_free_row(sheet)
    sheet.updateRow(row, list(movie_data.values()))
    print(f"Successfully added movie to row: {str(row)}")


if __name__ == "__main__":
    print("This is the core module.")
    user_args = read_user_cli_args()
    movie_data = extract_movie_data(
        get_movie_data(user_args.imdb_id[0]), user_args.watched, user_args.add
    )
    if user_args.view:
        print(f"Viewing movie info for {movie_data['Title']}.")
        show_info(movie_data)
    elif user_args.add:
        ss, sh = get_spreadsheet_and_sheet()
        print(f"Adding movie {movie_data['Title']} to spreadsheet {ss.title}.")
        add_to_sheet(movie_data, sh)
