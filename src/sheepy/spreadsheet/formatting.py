from typing import TYPE_CHECKING

from gspread.utils import ValueInputOption
from gspread_formatting import (
    BooleanCondition,
    CellFormat,
    DataValidationRule,
    TextFormat,
    format_cell_range,
    set_data_validation_for_cell_range,
)

from .sheet_util import (
    COLUMNS,
    SHEET_BACKGROUND_COLOR,
    SHEET_COLUMNS_RANGE,
    SHEET_HEADER_RANGE,
    SHEET_TEXT_COLOR,
)

if TYPE_CHECKING:
    from .spreadsheet import SheepySpreadsheet


def setup_sheet_formatting(ss: "SheepySpreadsheet") -> None:
    check_headers(ss)
    setup_sheet_text_and_color(ss)
    header_format(ss)


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


def setup_sheet_text_and_color(ss: "SheepySpreadsheet") -> None:
    fmt = CellFormat(
        backgroundColor=SHEET_BACKGROUND_COLOR,
        textFormat=TextFormat(foregroundColor=SHEET_TEXT_COLOR),
        horizontalAlignment="CENTER",
    )
    format_cell_range(ss.worksheet, SHEET_COLUMNS_RANGE, fmt)


def header_format(ss: "SheepySpreadsheet") -> None:
    fmt = CellFormat(
        textFormat=TextFormat(bold=True),
        horizontalAlignment="CENTER",
    )
    format_cell_range(ss.worksheet, SHEET_HEADER_RANGE, fmt)


def setup_checkboxes(
    ss: "SheepySpreadsheet", cell: str, validation: DataValidationRule = None
) -> None:
    if validation is None:
        validation = DataValidationRule(
            BooleanCondition("BOOLEAN", ["True", "False"]), showCustomUi=True
        )
    set_data_validation_for_cell_range(ss.worksheet, cell, validation)


def set_height_and_width(ss: "SheepySpreadsheet") -> None:
    pass
