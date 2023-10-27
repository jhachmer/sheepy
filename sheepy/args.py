"""Utility to parse User input from CLI"""

import argparse


def read_user_cli_args():
    """Handles the CLI user interactions.

    Returns:
        argparse.Namespace: Populated namespace object
    """
    parser = argparse.ArgumentParser(
        description="Add or view movies to your personal database."
    )
    parser.add_argument(
        "imdb_id", nargs=1, type=str, help="Enter the movies imdb id."
    )
    mut_req_group = parser.add_mutually_exclusive_group(required=True)
    mut_req_group.add_argument(
        "-a",
        "--add",
        action="store_true",
        help="Set to add to database (This or -v/--view is required)",
    )
    mut_req_group.add_argument(
        "-v",
        "--view",
        action="store_true",
        help="Set to view in the CLI (This or -a/--add is required)",
    )
    parser.add_argument(
        "-w",
        "--watched",
        action="store_true",
        help="Set to mark movie as already watched (Defaults to False)",
    )

    return parser.parse_args()
