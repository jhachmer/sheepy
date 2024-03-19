import argparse

from sheepy.core import create_new_sheet, view_movie_info


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

    return global_parser.parse_args()


def cli_new_sheet(args: argparse.Namespace) -> None:
    create_new_sheet(args.email[0])


def cli_view_movie(args: argparse.Namespace) -> None:
    view_movie_info(args.imdb_id[0])


def cli_add_movie(args: argparse.Namespace) -> None:
    print(args)
