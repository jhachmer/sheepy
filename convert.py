import logging
import os
from typing import Any

import gspread
from sheepy.omdbapi.omdb import process_movie_request_name_year
from sheepy.spreadsheet.spreadsheet import SheepySpreadsheet

SOURCE_SHEET_ID = os.getenv("S_S_ID")

if not os.path.exists("logs"):
    os.mkdir("logs")
    if not os.path.exists("logs/failed_to_parse.log"):
        open("logs/failed_to_parse.log", "w").close()


LOG_FORMAT = "[%(asctime)s] {%(filename)s:%(lineno)d} %(levelname)s - %(message)s"

conv_logger = logging.getLogger(__name__)
conv_logger.addHandler(logging.FileHandler(filename="logs/failed_to_parse.log"))


def log_failed_conversions(entry: list):
    conv_logger.info(f"Failed conversion: \n{entry}")


def read_name_and_year(
    source_sheet: SheepySpreadsheet, row_number: int
) -> tuple[str, int]:
    value_list: list[Any] = source_sheet.read_row(row_number)
    return value_list[1], value_list[2]


def get_number_of_rows(wks) -> int:
    row_list: list = list(filter(None, wks.col_values(2)))
    return len(row_list) + 1


if __name__ == "__main__":
    gc = gspread.service_account()

    if SOURCE_SHEET_ID is None:
        raise SystemExit("env variable not set")
    sh: gspread.Spreadsheet = gc.open_by_key(SOURCE_SHEET_ID)
    wks: gspread.Worksheet = sh.get_worksheet(0)

    target_sheet: SheepySpreadsheet = SheepySpreadsheet.from_env_file()

    num_of_rows = get_number_of_rows(wks) - 1

    list_of_lists = wks.get_all_values(range_name=f"A2:C{num_of_rows}")

    # print(list_of_lists)

    for entry in list_of_lists:
        try:
            add = True if entry[0] == "TRUE" else False
            movie_data = process_movie_request_name_year(entry[1], entry[2], add)
            # show_info(movie_data)
            target_sheet.add_values_to_sheet(movie_data)
        except SystemExit:
            log_failed_conversions(entry)
            continue
