from gspread.utils import ValueInputOption, rowcol_to_a1

from sheepy.spreadsheet.spreadsheet import SheepySpreadsheet


def add_movie_to_sheet(ss: SheepySpreadsheet, movie_dict: dict[str, str]) -> None:
    """Adds movie to spreadsheet

    Args:
        ss (SheepySpreadsheet): Google Spreadsheet instance
        movie_dict (dict): Dictionary with movie data
    """
    if ss.spreadsheet.worksheet is None:
        raise ValueError("Select a worksheet first")
    insert_row: int = ss.spreadsheet.find_free_row()
    a1_notation: str = rowcol_to_a1(insert_row, 1)
    values: list = [list(movie_dict.values())]
    ss.logger.info("A1-Notation %s", a1_notation)
    ss.logger.info("%s", values)
    ss.spreadsheet.worksheet.update(
        range_name=a1_notation,
        values=values,
        value_input_option=ValueInputOption.user_entered,
    )
