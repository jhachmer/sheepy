from sheepy.util.cli import read_user_cli_args
from sheepy.util.logger import get_logger


def main() -> None:
    """
    Main entry for cli logic
    """
    logger = get_logger(__name__)
    logger.info("Entry")
    args = read_user_cli_args()
    logger.info(args)

    """
    sheepy_sheet: SheepySpreadsheet = get_env_spreadsheet()
    setup_columns(sheepy_sheet)
    movie_info: dict = add_movie_to_sheet(
        ss=sheepy_sheet, imdb_id=args.imdb_id[0], watched=args.watched, add=args.add
    )
    logger.info(
        f"\n{'#'*60}\n"
        f"Added Movie Info: {movie_info}\n"
        f"to Spreadsheet:\n{sheepy_sheet}\n"
        f"{'#'*60}\n"
    )
    """
    args.func(args)


if __name__ == "__main__":
    main()
