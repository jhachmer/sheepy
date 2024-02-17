from sheepy import SheepySpreadsheet
from gspread.utils import rowcol_to_a1, ValueInputOption

from sheepy.util.logger import get_logger


class Client:

    def __init__(self, ss: SheepySpreadsheet):
        self.spreadsheet = ss
        self.logger = get_logger(__name__)

    def add_movie_to_sheet(self, movie_dict: dict[str, str]) -> None:
        """Adds movie to spreadsheet

        Args:
            movie_dict (dict): Dictionary with movie data
        """
        if self.spreadsheet.worksheet is None:
            raise ValueError("Select a worksheet first")
        insert_row: int = self.spreadsheet.find_free_row()
        a1_notation: str = rowcol_to_a1(insert_row, 1)
        values: list = [list(movie_dict.values())]
        self.logger.info("A1-Notation %s", a1_notation)
        self.logger.info("%s", values)
        self.spreadsheet.worksheet.update(
            range_name=a1_notation,
            values=values,
            value_input_option=ValueInputOption.user_entered,
        )
