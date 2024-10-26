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
