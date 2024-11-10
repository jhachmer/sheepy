import sys

from sheepy.omdb.api import process_movie_request_imdb_id, show_info
from sheepy.spreadsheet.spreadsheet import SheepySpreadsheet
from sheepy.util.exceptions import MovieRetrievalError
from sheepy.util.logger import get_logger

core_logger = get_logger(__name__)


def add_movie_to_sheet(
    ss: SheepySpreadsheet,
    imdb_id: str,
    watched: bool = False,
) -> None:
    """
    Add a movie to a Spreadsheet

    Args:
        ss (SheepySpreadsheet): SheepySpreadsheet instance
        imdb_id (str): IMDB ID of movie
        watched (bool, optional): Whether to tick watched checkbox
    """
    try:
        insert_data: dict[str, str] = process_movie_request_imdb_id(
            imdb_id, watched, True
        )
    except MovieRetrievalError:
        core_logger.error("Error. Exiting...")
        sys.exit(-1)
    ss.add_values_to_sheet(insert_data)


def view_movie_info(imdb_id: str) -> None:
    """
    Displays movie information in a table

    Args:
        imdb_id: IMDB ID of movie
    """
    try:
        view_data: dict[str, str] = process_movie_request_imdb_id(imdb_id, False, False)
    except MovieRetrievalError:
        core_logger.error("Error. Exiting...")
        sys.exit(-1)
    print(show_info(view_data))


def download_csv(ss: SheepySpreadsheet) -> None:
    """Downloads Google Spreadsheet in csv format

    Args:
        ss (SheepySpreadsheet): SheepySpreadsheet instance
    """
    ss.download_csv()


def get_spreadsheet(ss_id: str, ws_idx: str) -> SheepySpreadsheet:
    """
    Get a Spreadsheet by id

    Args:
        ss_id (str): Spreadsheet ID. Taken from URL
        ws_idx (str): Index of worksheet in spreadsheet

    Returns:
        SheepySpreadsheet: Spreadsheet instance
    """
    return SheepySpreadsheet(ss_id, ws_idx)


def create_new_sheet(email: str) -> SheepySpreadsheet:
    """
    Create a new Spreadsheet

    Args:
        email (str): Email to share spreadsheet with

    Returns:
        SheepySpreadsheet: Spreadsheet instance
    """
    ss: SheepySpreadsheet = SheepySpreadsheet.from_new()
    ss.logger.info(
        f"Created new sheet\nSpreadsheet ID: {ss.spreadsheet_id}\n"
        f"Worksheet Index: {ss.worksheet_index}"
    )
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
    ss.share_spreadsheet(email, "user", "writer")
    return ss


def get_env_spreadsheet() -> SheepySpreadsheet:
    """
    Get a Spreadsheet from env-file config

    Returns:
        SheepySpreadsheet: Spreadsheet instance
    """
    return SheepySpreadsheet.from_env_file()


def _view_and_add_from_clipboard(imdb_id: str):
    ss: SheepySpreadsheet = SheepySpreadsheet.from_env_file()
    core_logger.info(f"Found IMDb entry from ID: {imdb_id}")
    print("Adding to Spreadsheet...")
    add_movie_to_sheet(ss=ss, imdb_id=imdb_id)
    print("Done!")


def watch_clipboard() -> None:
    """
    Watches Clipboard for valid IMDb Ids
    """
    watcher: ClipboardWatcher = ClipboardWatcher(
        check_for_imdb_id, _view_and_add_from_clipboard, 1.0
    )
    watcher.start()
    print("Waiting for clipboard contents...")
    print("Press Ctrl+C in terminal window to exit.")
    while True:
        try:
            print("...")
            time.sleep(10)
        except KeyboardInterrupt:
            print("Exiting...")
            watcher.stop()
            break
