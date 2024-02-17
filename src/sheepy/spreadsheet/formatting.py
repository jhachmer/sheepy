from gspread.utils import ValueInputOption

from sheepy.spreadsheet.sheet_utils import COLUMNS
from sheepy.spreadsheet.spreadsheet import SheepySpreadsheet


def setup_sheet_formatting(ss: SheepySpreadsheet) -> None:
    pass


def setup_headers(ss: SheepySpreadsheet) -> None:
    """Sets up Sheet Headers, defined in class constant HEADERS
    Raises:
        ValueError: Raises Exception if no worksheet is selected
    """
    if ss.worksheet is None:
        raise ValueError("Select a worksheet first")
    ss.logger.info("Updating Headers")
    ss.worksheet.update(
        range_name="A1",
        values=[list(COLUMNS)],
        value_input_option=ValueInputOption.user_entered,
    )


def check_headers(ss: SheepySpreadsheet) -> None:
    """Checks if Sheet has correct headers
    Raises:
        ValueError: Raises Exception if no worksheet is selected
    """
    if ss.worksheet is None:
        raise ValueError("Select a worksheet first")
    values_list = ss.worksheet.row_values(1)
    if COLUMNS != values_list:
        ss.logger.info("Headers need updating")
        setup_headers(ss)
