import argparse
import logging

from sheepy.cli.cli import read_user_cli_args
from sheepy.util.logger import get_logger


def main() -> None:
    """
    Main entry for application
    """
    logger: logging.Logger = get_logger(__name__)
    print("\N{SNAKE}\N{SNAKE} Hello, welcome to Sheepy \N{SNAKE}\N{SNAKE}\n")
    args: argparse.Namespace = read_user_cli_args()
    logger.debug(args)

    args.func(args)


if __name__ == "__main__":
    main()
