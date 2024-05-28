from sheepy.util.cli import read_user_cli_args
from sheepy.util.logger import get_logger


def main() -> None:
    """
    Main entry for cli logic
    """
    logger = get_logger(__name__)
    print("Hello there, welcome to Sheepy :)\N{snake}\N{snake}\N{snake}\n")
    args = read_user_cli_args()
    logger.debug(args)

    args.func(args)


if __name__ == "__main__":
    main()
