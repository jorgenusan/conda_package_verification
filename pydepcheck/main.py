import argparse

from pydepcheck.cli import CLI


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Update environment files")
    parser.add_argument(
        "-ef", "--env-file", type=str, help="Path to the environment file"
    )
    parser.add_argument("-en", "--env-name", type=str, help="Conda environment name")
    parser.add_argument("files", nargs="*", help="Files to be committed (ignored)")
    args = parser.parse_args()

    return args


def main() -> None:
    args = parse_args()

    cpv_cli = CLI(args.env_file, args.env_name)
    cpv_cli.run()


if __name__ == "__main__":
    main()
