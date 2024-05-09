import argparse
import sys

from utils.utils import get_file_hash

from pydepcheck.cli import CLI


def main() -> None:
    parser = argparse.ArgumentParser(description="Update environment files")
    parser.add_argument(
        "-ef", "--env_file", type=str, help="Path to the environment file"
    )
    parser.add_argument("-en", "--env_name", type=str, help="Conda environment name")
    parser.add_argument("files", nargs="*", help="Files to be committed (ignored)")
    args = parser.parse_args()

    initial_hash = get_file_hash(args.env_file)

    cpv_cli = CLI(args.env_file, args.env_name)
    cpv_cli.run()

    final_hash = get_file_hash(args.env_file)
    print(initial_hash)
    print(final_hash)
    if initial_hash != final_hash:
        sys.exit(1)


if __name__ == "__main__":
    main()
