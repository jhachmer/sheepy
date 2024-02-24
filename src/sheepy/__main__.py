from sheepy import SheepySpreadsheet
from sheepy.core import get_env_spreadsheet, process_movie_request
from sheepy.util.cli import read_user_cli_args
from sheepy.util.logger import get_logger


def main() -> None:
    """
    Main entry for cli logic
    """
    logger = get_logger(__name__)
    logger.info("Entry")
    args = read_user_cli_args()
    logger.debug(args)
    movie_info: dict = process_movie_request(
        imdb_id=args.imdb_id[0], watched=args.watched, add=args.add
    )
    sheepy_sheet: SheepySpreadsheet = get_env_spreadsheet()
    sheepy_sheet.add_values_to_sheet(movie_info)
    logger.info(f"{'-'*40}\n"
                f"Added Movie Info: {movie_info}\n"
                f"to Spreadsheet:\n{sheepy_sheet}\n"
                f"{'-'*40}")


if __name__ == "__main__":
    main()
