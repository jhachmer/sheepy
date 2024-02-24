from sheepy import SheepySpreadsheet, process_movie_request


def add_movie_to_sheet(
    ss: SheepySpreadsheet, imdb_id: str, watched: bool = False, add: bool = True
):
    """
    Add a movie to a Spreadsheet
    Args:
        ss (SheepySpreadsheet): SheepySpreadsheet instance
        imdb_id (str): IMDB ID of movie
        watched (bool, optional): Whether to tick watched checkbox
        add (bool, optional): Whether to add a movie or show info in cli (NYI)
    """
    insert_data: dict[str, str] = process_movie_request(imdb_id, watched, add)
    ss.add_values_to_sheet(insert_data)


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
    ss.share_spreadsheet(email, "user", "writer")
    return ss


def get_env_spreadsheet() -> SheepySpreadsheet:
    """
    Get a Spreadsheet from env-file config
    Returns:
        SheepySpreadsheet: Spreadsheet instance
    """
    return SheepySpreadsheet.from_env_file()


if __name__ == "__main__":
    ss_test: SheepySpreadsheet = get_spreadsheet(
        "10cl4nHYqSc1Yk9M4c7gA5OF2aUX8IdN26ViBot76vA0", "0"
    )
    add_movie_to_sheet(ss_test, "tt15239678", watched=True, add=True)
