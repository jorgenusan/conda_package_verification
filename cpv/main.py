import argparse

from cpv.cpv_cli import CPVCLI


def main() -> None:
    parser = argparse.ArgumentParser(description="Update environment files")
    parser.add_argument(
        "-ef", "--env_file", type=str, help="Path to the environment file"
    )
    parser.add_argument("-en", "--env_name", type=str, help="Conda environment name")
    parser.add_argument("files", nargs="*", help="Files to be committed (ignored)")
    args = parser.parse_args()

    cpv_cli = CPVCLI(args.env_file, args.env_name)
    cpv_cli.run()


if __name__ == "__main__":
    main()
