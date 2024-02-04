"""YOU PROBABLY SHOULDNT USE THIS"""

import logging
import os
import sys
import time
import urllib

import ezsheets
import requests
from dotenv import load_dotenv

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

load_dotenv()

API_KEY = os.environ.get("OMDB_API_KEY", "")
CONVERT_ID = os.environ.get("CONVERT_ID", "")
ROW_INCR = 2
URL = "http://www.omdbapi.com/?apikey="


def convert(row: list) -> list:
    """
    Converts old format of movie data into a list new format of movie data using the OMDb API.

    Args:
        row (list): A list of movie data.

    Returns:
        list: A list of movie information.

    Raises:
        SystemExit: If there is an HTTP error or a request exception.
    """
    movie_search_data = (row[1], row[2])
    try:
        response = requests.get(
            # flake8: noqa E501
            f"{URL}{API_KEY}&t={urllib.parse.quote(movie_search_data[0])}&y={movie_search_data[1]}"
        )
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

    md = response.json()
    if md["Response"] == "False":
        logger.error(f"{md['Error']} - Invalid IMDb ID. Please try again.")
        logger.error(f"Failed to parse: {movie_search_data[0]}")
        with open("logs/failed_to_parse.txt", "a") as f:
            f.write(f"Failed to parse: {movie_search_data[0]} ({movie_search_data[1]}) \n")
        raise SystemExit(f"{md['Error']} - Invalid IMDb ID. Please try again.")

    print(
        [
            row[0],
            md["Title"],
            md["Year"],
            md["Genre"],
            md["Runtime"],
            row[4],
            md["imdbRating"].replace(".", ","),
            md["Ratings"][1]["Value"] if len(md["Ratings"]) > 1 else "N/A",
            md["Director"],
            md["Plot"],
            md["Poster"],
        ]
    )
    return [
        row[0],
        md["Title"],
        md["Year"],
        md["Genre"],
        md["Runtime"],
        row[4],
        md["imdbRating"].replace(".", ","),
        md["Ratings"][1]["Value"],
        md["Director"],
        md["Plot"],
        f"=IMAGE(\"{md['Poster']}\")" if len(md["Ratings"]) > 1 else "N/A",
    ]


def get_convert_sheet(ss_id: str = CONVERT_ID) -> ezsheets.Sheet:
    """
    Returns the first sheet of a Google Spreadsheet with the given ID.

    Args:
        ss_id (str): The ID of the Google Spreadsheet to retrieve the sheet from.
            Defaults to the CONVERT_ID constant defined in the module.

    Returns:
        ezsheets.Sheet: The first sheet of the specified Google Spreadsheet.
    """
    return ezsheets.Spreadsheet(ss_id).sheets[0]


def get_entry(sheet: ezsheets.Sheet) -> list:
    """
    Generator function that yields each row of data from the given sheet, starting from the second row.

    Args:
        sheet (ezsheets.Sheet): The sheet to extract data from.

    Yields:
        list: A list containing the values of each cell in the current row.
    """
    rows = sheet.getRows()
    for row in rows[1:]:
        yield row


def add_entry(sheet: ezsheets.Sheet, row_number: int, entry: list):
    """
    Adds an entry to the specified row of a Google Sheet.

    Args:
        sheet (ezsheets.Sheet): The Google Sheet to add the entry to.
        row_number (int): The row number to add the entry to.
        entry (list): The entry to add to the row.

    Returns:
        None
    """
    sheet.updateRow(row_number, entry)


if __name__ == "__main__":
    convert_sheet = get_convert_sheet()

    for row_number, entry in enumerate(get_entry(convert_sheet)):
        time.sleep(0.4)
        if entry[1] == "":
            break
        try:
            new_row = convert(entry)
            add_entry(convert_sheet, row_number + ROW_INCR, new_row)
        except SystemExit as se:
            with open("logs/failed_to_parse.txt", "a") as f:
                f.write(f"Failed to parse: {entry[1]} ({entry[2]}) \n")
            continue
        except Exception as e:
            with open("logs/failed_to_parse.txt", "a") as f:
                f.write(f"Failed to parse: {entry[1]} ({entry[2]}) \n")
            logger.error(f"General Error: {str(e)}")
            continue
