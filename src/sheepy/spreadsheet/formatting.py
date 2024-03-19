from typing import TYPE_CHECKING

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
    COLUMNS,
    SHEET_BACKGROUND_COLOR_EVEN,
    SHEET_BACKGROUND_COLOR_ODD,
    SHEET_COL_A_WIDTH,
    SHEET_COL_B_WIDTH,
    SHEET_COL_C_WIDTH,
    SHEET_COL_D_WIDTH,
    SHEET_COL_E_WIDTH,
    SHEET_COL_F_WIDTH,
    SHEET_COL_G_WIDTH,
    SHEET_COL_H_WIDTH,
    SHEET_COL_I_WIDTH,
    SHEET_COL_J_WIDTH,
    SHEET_COL_K_WIDTH,
    SHEET_HEADER_RANGE,
    SHEET_PLOT_COL,
    SHEET_ROW_HEIGHT,
    SHEET_TEXT_COLOR,
)

if TYPE_CHECKING:
    from .spreadsheet import SheepySpreadsheet


def setup_sheet_formatting(ss: "SheepySpreadsheet") -> None:
    check_headers(ss)
    setup_sheet_text_and_color(ss)
    header_format(ss)
    setup_columns(ss)


def setup_headers(ss: "SheepySpreadsheet") -> None:
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
    _freeze_header_row(ss)


def check_headers(ss: "SheepySpreadsheet") -> None:
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


# noinspection PyTestUnpassedFixture
def setup_sheet_text_and_color(ss: "SheepySpreadsheet") -> None:
    """
    Sets up Sheet Background Color and Text Color

    Args:
        ss (SheepySpreadsheet): Spreadsheet object
    """
    fmt_odd = CellFormat(
        backgroundColor=SHEET_BACKGROUND_COLOR_ODD,
        textFormat=TextFormat(foregroundColor=SHEET_TEXT_COLOR),
        horizontalAlignment="CENTER",
    )
    fmt_even = CellFormat(
        backgroundColor=SHEET_BACKGROUND_COLOR_EVEN,
        textFormat=TextFormat(foregroundColor=SHEET_TEXT_COLOR),
        horizontalAlignment="CENTER",
    )
    # TODO: Black/Gray Alternating Background
    batch: SpreadsheetBatchUpdater = SpreadsheetBatchUpdater(ss.spreadsheet)
    batch.format_cell_range(ss.worksheet, "A", fmt_odd)
    batch.format_cell_range(ss.worksheet, "B", fmt_even)
    batch.format_cell_range(ss.worksheet, "C", fmt_odd)
    batch.format_cell_range(ss.worksheet, "D", fmt_even)
    batch.format_cell_range(ss.worksheet, "E", fmt_odd)
    batch.format_cell_range(ss.worksheet, "F", fmt_even)
    batch.format_cell_range(ss.worksheet, "G", fmt_odd)
    batch.format_cell_range(ss.worksheet, "H", fmt_even)
    batch.format_cell_range(ss.worksheet, "I", fmt_odd)
    batch.format_cell_range(ss.worksheet, "J", fmt_even)
    batch.format_cell_range(ss.worksheet, "K", fmt_odd)
    batch.format_cell_range(ss.worksheet, "L", fmt_even)
    batch.execute()


def header_format(ss: "SheepySpreadsheet") -> None:
    """
    Sets up Header Row (Row 1)
    Args:
        ss (SheepySpreadsheet): Spreadsheet object
    """
    fmt = CellFormat(
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
        cell: Cell to put Checkbox
        validation: DataValidation rule (Default value = None)
    """
    if validation is None:
        validation = DataValidationRule(
            BooleanCondition("BOOLEAN", ["True", "False"]), showCustomUi=True
        )
    set_data_validation_for_cell_range(ss.worksheet, cell, validation)


def _freeze_header_row(ss: "SheepySpreadsheet", row: int = 1) -> None:
    set_frozen(ss.worksheet, rows=row)


def set_insert_row_height(ss: "SheepySpreadsheet", row: int) -> None:
    batch: SpreadsheetBatchUpdater = SpreadsheetBatchUpdater(ss.spreadsheet)
    ws = ss.worksheet
    # Set height of row
    batch.set_row_height(ws, f"{row}", SHEET_ROW_HEIGHT)
    batch.execute()


# noinspection PyTestUnpassedFixture
def setup_columns(ss: "SheepySpreadsheet") -> None:
    batch: SpreadsheetBatchUpdater = SpreadsheetBatchUpdater(ss.spreadsheet)
    cf: CellFormat = CellFormat(wrapStrategy="WRAP", verticalAlignment="MIDDLE")
    ws: gspread.Worksheet = ss.worksheet
    batch.set_column_width(ws, *SHEET_COL_A_WIDTH)
    batch.set_column_width(ws, *SHEET_COL_B_WIDTH)
    batch.set_column_width(ws, *SHEET_COL_C_WIDTH)
    batch.set_column_width(ws, *SHEET_COL_D_WIDTH)
    batch.set_column_width(ws, *SHEET_COL_E_WIDTH)
    batch.set_column_width(ws, *SHEET_COL_F_WIDTH)
    batch.set_column_width(ws, *SHEET_COL_G_WIDTH)
    batch.set_column_width(ws, *SHEET_COL_H_WIDTH)
    batch.set_column_width(ws, *SHEET_COL_I_WIDTH)
    batch.set_column_width(ws, *SHEET_COL_J_WIDTH)
    batch.set_column_width(ws, *SHEET_COL_K_WIDTH)
    batch.format_cell_range(ws, SHEET_PLOT_COL, cf)
    batch.execute()
