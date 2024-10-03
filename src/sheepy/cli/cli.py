import argparse
import sys

from sheepy.core import (
    add_movie_to_sheet,
    create_new_sheet,
    download_csv,
    get_env_spreadsheet,
    view_movie_info,
)
from sheepy.spreadsheet.spreadsheet import SheepySpreadsheet


def read_user_cli_args() -> argparse.Namespace:
    """Handles the CLI user interactions.

    Returns:
        argparse.Namespace: Populated namespace object
    """
    global_parser = argparse.ArgumentParser(
        description="Add or view movies to your personal database.", prog="sheepy"
    )

    subparsers = global_parser.add_subparsers(
        title="subcommands", help="Commands offered by sheepy"
    )

    new_parser = subparsers.add_parser("new", help="Create a new sheet")
    new_parser.add_argument(
        "email", nargs=1, type=str, help="Enter E-Mail Address of Google Account."
    )
    new_parser.set_defaults(func=cli_new_sheet)

    view_parser = subparsers.add_parser("view", help="View Movie Info")
    view_parser.add_argument(
        "imdb_id", nargs=1, type=str, help="Enter the movies imdb id to view."
    )
    view_parser.set_defaults(func=cli_view_movie)

    add_parser = subparsers.add_parser("add", help="Add Movie to Sheet")
    add_parser.add_argument(
        "imdb_id", nargs=1, type=str, help="Enter the movies imdb id to add."
    )
    add_parser.add_argument(
        "-w",
        "--watched",
        action="store_true",
        help="Set to mark movie as already watched (Defaults to False)",
    )
    add_parser.set_defaults(func=cli_add_movie)
    dl_parser = subparsers.add_parser("dl", help="Download spreadsheet as csv")
    dl_parser.set_defaults(func=cli_download_csv)

    return global_parser.parse_args(args=None if sys.argv[1:] else ["--help"])


def cli_new_sheet(args: argparse.Namespace) -> None:
    """
    Creates a new sheet when new command is used

    Args:
        args (argparse.Namespace): Arguments parsed from command line
    """
    create_new_sheet(args.email[0])


def cli_view_movie(args: argparse.Namespace) -> None:
    """
    Displays movie information when view command is used

    Args:
        args (argparse.Namespace): Arguments parsed from command line
    """
    view_movie_info(args.imdb_id[0])


def cli_add_movie(args: argparse.Namespace) -> None:
    """
    Adds movie to sheet when add command is used

    Args:
        args (argparse.Namespace): Arguments parsed from command line
    """
    ss: SheepySpreadsheet = get_env_spreadsheet()
    add_movie_to_sheet(ss=ss, imdb_id=args.imdb_id[0], watched=args.watched)


def cli_download_csv(args: argparse.Namespace) -> None:
    """Downloads Google Spreadsheet in csv format

    Args:
        args (argparse.Namespace): Arguments parsed from command line
    """
    ss: SheepySpreadsheet = get_env_spreadsheet()
    download_csv(ss)
