from sheepy.util.cli import read_user_cli_args


def main() -> None:
    parsed_args = read_user_cli_args()
    print(parsed_args)
    print("Test")


if __name__ == "__main__":
    main()
