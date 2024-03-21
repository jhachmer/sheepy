from sheepy.omdbapi.omdb import process_movie_request, show_info
from sheepy.spreadsheet.spreadsheet import SheepySpreadsheet


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
    insert_data: dict[str, str] = process_movie_request(imdb_id, watched, True)
    ss.add_values_to_sheet(insert_data)


def view_movie_info(imdb_id: str) -> None:
    """
    Displays movie information in a table

    Args:
        imdb_id: IMDB ID of movie
    """
    view_data: dict[str, str] = process_movie_request(imdb_id, False, False)
    show_info(view_data)


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
