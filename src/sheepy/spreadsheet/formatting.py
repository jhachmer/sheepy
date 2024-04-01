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

from .sheet_util import (
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
    fmt_odd: CellFormat = CellFormat(
        backgroundColor=SHEET_BACKGROUND_COLOR_ODD,
        textFormat=TextFormat(foregroundColor=SHEET_TEXT_COLOR),
        horizontalAlignment="CENTER",
        verticalAlignment="MIDDLE",
    )
    fmt_even: CellFormat = CellFormat(
        backgroundColor=SHEET_BACKGROUND_COLOR_EVEN,
        textFormat=TextFormat(foregroundColor=SHEET_TEXT_COLOR),
        horizontalAlignment="CENTER",
        verticalAlignment="MIDDLE",
    )
    batch: SpreadsheetBatchUpdater = SpreadsheetBatchUpdater(ss.spreadsheet)
    # convert ascii numbers to column names
    for i in range(65, 77):
        if (i % 2) == 1:
            batch.format_cell_range(ss.worksheet, chr(i), fmt_odd)
        else:
            batch.format_cell_range(ss.worksheet, chr(i), fmt_even)
    batch.execute()


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
    ss: "SheepySpreadsheet", cell: str, validation: DataValidationRule = None
) -> None:
    """
    Sets up Checkboxes for watched value

    Args:
        ss (SheepySpreadsheet): Spreadsheet object
        cell (str): Cell to put Checkbox
        validation (DataValidationRule): DataValidation rule (Default value = None)
    """
    if validation is None:
        validation = DataValidationRule(
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
    batch: SpreadsheetBatchUpdater = SpreadsheetBatchUpdater(ss.spreadsheet)
    ws: gspread.Worksheet = ss.worksheet
    # Set height of row
    batch.set_row_height(ws, f"{row}", SHEET_ROW_HEIGHT)
    batch.execute()


# noinspection PyTestUnpassedFixture
def setup_columns(ss: "SheepySpreadsheet") -> None:
    """
    Sets column widths for columns used for values

    Args:
        ss (SheepySpreadsheet): Spreadsheet object
    """
    batch: SpreadsheetBatchUpdater = SpreadsheetBatchUpdater(ss.spreadsheet)
    cf: CellFormat = CellFormat(wrapStrategy="WRAP", verticalAlignment="MIDDLE")
    ws: gspread.Worksheet = ss.worksheet

    for format_tuple in COLUMN_WIDTHS:
        batch.set_column_width(ws, **format_tuple)

    batch.format_cell_range(ws, SHEET_PLOT_COL, cf)
    batch.execute()
