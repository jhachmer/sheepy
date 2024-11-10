import os
from logging import Logger

from sheepy.util.logger import get_logger

logger: Logger = get_logger(__name__)


def delete_csv(filename: str = "sheepy.csv") -> None:
    """Deletes downloaded CSV-file from the filesystem"""
    try:
        os.remove(filename)
    except FileNotFoundError as fnfe:
        logger.info(f"Unable to delete Spreadsheet file\n{fnfe}")
        logger.debug(fnfe)


def rename_file(new_name: str, orig_file: str = "sheepy.csv") -> None:
    """Renames (spreadsheet) file

    Args:
        new_name (str): _description_
        orig_file (str, optional): _description_. Defaults to "sheepy.csv".
    """
    try:
        os.rename(orig_file, new_name)
    except FileNotFoundError as fnfe:
        logger.info(f"Unable to delete Spreadsheet file\n{fnfe}")
        logger.debug(fnfe)


def create_env_file(ss):
    ss.logger.info(
        "Make Sure to fill out remaining fields in .env file."
        " After filling out rename to '.env'"
    )
    with open("new.env", "x") as env_file:
        env_file.write(
            "# OMDB API KEY\n"
            'OMDB_API_KEY="Your_API_Key"\n'
            "# GOOGLE SHEETS ID\n"
            "# LONG STRING IN THE URL AFTER /d/ AND BEFORE /edit\n"
            f'SPREADSHEET_ID="{ss.spreadsheet_id}"\n'
            "\n"
            f'WORKSHEET_INDEX="{ss.worksheet_index}"\n'
            "\n"
            "# ENTER YOUR NAME HERE :)\n"
            'SUGGESTED_BY="Your_Name"\n'
        )
