import argparse

from cpv.cpv_cli import CPVCLI


def main(env_file: str, conda_env: str) -> None:
    cpv_cli = CPVCLI(env_file, conda_env)
    cpv_cli.run()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Update environment files")
    parser.add_argument(
        "-ef", "--env_file", type=str, help="Path to the environment file"
    )
    parser.add_argument(
        "-ce", "--conda_env", type=str, help="Path to the conda environment file"
    )
    args = parser.parse_args()

    main(args.env_file, args.conda_env)
