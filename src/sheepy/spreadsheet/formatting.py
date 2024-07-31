from typing import TYPE_CHECKING, Any

import gspread
from gspread.utils import ValueInputOption
from gspread_formatting import (
    BooleanCondition,
    CellFormat,
    DataValidationRule,
    SpreadsheetBatchUpdater,
    TextFormat,
    format_cell_range,
    set_data_validation_for_cell_range,
    set_frozen,
)

from .sheet_config import (
    COLUMN_WIDTHS,
    COLUMNS,
    SHEET_BACKGROUND_COLOR_EVEN,
    SHEET_BACKGROUND_COLOR_ODD,
    SHEET_HEADER_RANGE,
    SHEET_PLOT_COL,
    SHEET_ROW_HEIGHT,
    SHEET_TEXT_COLOR,
)

if TYPE_CHECKING:
    from .spreadsheet import SheepySpreadsheet


# TODO: Title, Genre, Plot left-aligned
# TODO: Custom Image width/height


def setup_sheet_formatting(ss: "SheepySpreadsheet") -> None:
    """
    Setup sheet formatting
    Calling other functions to set up individual parts

    Args:
        ss (SheepySpreadsheet): Spreadsheet object
    """
    check_headers(ss)
    setup_sheet_text_and_color(ss)
    header_format(ss)
    setup_columns(ss)


def setup_headers(ss: "SheepySpreadsheet") -> None:
    """Sets up Sheet Headers, defined in class constant HEADERS

    Args:
        ss (SheepySpreadsheet): Spreadsheet object

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
    _freeze_header_row(ss)


def check_headers(ss: "SheepySpreadsheet") -> None:
    """Checks if Sheet has correct headers

    Args:
        ss (SheepySpreadsheet): Spreadsheet object

    Raises:
        ValueError: Raises Exception if no worksheet is selected
    """
    if ss.worksheet is None:
        raise ValueError("Select a worksheet first")
    values_list: list[Any] = ss.worksheet.row_values(1)
    if COLUMNS != values_list:
        ss.logger.info("Headers need updating")
        setup_headers(ss)


# noinspection PyTestUnpassedFixture
def setup_sheet_text_and_color(ss: "SheepySpreadsheet") -> None:
    """
    Sets up Sheet Background Color and Text Color

    Args:
        ss (SheepySpreadsheet): Spreadsheet object
    """
    fmt_center: CellFormat = CellFormat(
        backgroundColor=SHEET_BACKGROUND_COLOR_EVEN,
        textFormat=TextFormat(foregroundColor=SHEET_TEXT_COLOR),
        horizontalAlignment="CENTER",
        verticalAlignment="MIDDLE",
    )
    fmt_left_align: CellFormat = CellFormat(
        backgroundColor=SHEET_BACKGROUND_COLOR_EVEN,
        textFormat=TextFormat(foregroundColor=SHEET_TEXT_COLOR),
        horizontalAlignment="LEFT",
        verticalAlignment="MIDDLE",
    )
    batch: SpreadsheetBatchUpdater = SpreadsheetBatchUpdater(ss.spreadsheet)
    # convert ascii numbers to column names
    for i in range(65, 77):
        if chr(i) in ["B", "D", "J"]:
            batch.format_cell_range(ss.worksheet, chr(i), fmt_left_align)  # type: ignore
        else:
            batch.format_cell_range(ss.worksheet, chr(i), fmt_center)  # type: ignore
    batch.execute()


def color_odd_rows(ss: "SheepySpreadsheet", row: int, nth: int) -> None:
    """Changes color of every nth row to value specified
     in sheet_config.py (SHEET_BACKGROUND_COLOR_ODD)

    Args:
        ss (SheepySpreadsheet): Spreadsheet object
        row (int): number of current row
        nth (int): number of every nth row to be colored
    """
    if row % nth == 0:
        gray_row: CellFormat = CellFormat(backgroundColor=SHEET_BACKGROUND_COLOR_ODD)
        format_cell_range(ss.worksheet, f"A{row}:L{row}", gray_row)


def header_format(ss: "SheepySpreadsheet") -> None:
    """
    Sets up Header Row (Row 1)

    Args:
        ss (SheepySpreadsheet): Spreadsheet object
    """
    fmt: CellFormat = CellFormat(
        textFormat=TextFormat(bold=True),
        horizontalAlignment="CENTER",
    )
    format_cell_range(ss.worksheet, SHEET_HEADER_RANGE, fmt)
    _freeze_header_row(ss)


def setup_checkboxes(
    ss: "SheepySpreadsheet",
    cell: str,
) -> None:
    """
    Sets up Checkboxes for watched value

    Args:
        ss (SheepySpreadsheet): Spreadsheet object
        cell (str): Cell to put Checkbox
    """
    validation: DataValidationRule = DataValidationRule(
        BooleanCondition("BOOLEAN", ["True", "False"]), showCustomUi=True
    )
    set_data_validation_for_cell_range(ss.worksheet, cell, validation)


def _freeze_header_row(ss: "SheepySpreadsheet", row: int = 1) -> None:
    """
    Freezes header row
    (stays fixed to top when scrolling)

    Args:
        ss (SheepySpreadsheet): Spreadsheet object
        row (int, optional): Row number to freeze. Defaults to 1
    """
    set_frozen(ss.worksheet, rows=row)


def set_insert_row_height(ss: "SheepySpreadsheet", row: int) -> None:
    """
    Sets row height for given row

    Args:
        ss (SheepySpreadsheet): Spreadsheet object
        row (int, optional): Row number
    """
    if ss.worksheet is None:
        raise ValueError("Worksheet of SheepySpreadsheet object is not set.")
    batch: SpreadsheetBatchUpdater = SpreadsheetBatchUpdater(ss.spreadsheet)
    ws: gspread.Worksheet = ss.worksheet
    # Set height of row
    batch.set_row_height(ws, f"{row}", SHEET_ROW_HEIGHT)  # type: ignore
    batch.execute()


# noinspection PyTestUnpassedFixture
def setup_columns(ss: "SheepySpreadsheet") -> None:
    """
    Sets column widths for columns used for values

    Args:
        ss (SheepySpreadsheet): Spreadsheet object
    """
    if ss.worksheet is None:
        raise ValueError("Worksheet of SheepySpreadsheet object is not set.")
    batch: SpreadsheetBatchUpdater = SpreadsheetBatchUpdater(ss.spreadsheet)
    cf: CellFormat = CellFormat(wrapStrategy="WRAP", verticalAlignment="MIDDLE")
    ws: gspread.Worksheet = ss.worksheet

    for format_tuple in COLUMN_WIDTHS:
        # col, width = format_tuple
        batch.set_column_width(ws, *format_tuple)  # type: ignore

    batch.format_cell_range(ws, SHEET_PLOT_COL, cf)  # type: ignore
    batch.execute()
