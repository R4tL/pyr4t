import argparse

from . import run_tests


def main():
    parser = argparse.ArgumentParser(
        description="Project utility CLI for common development tasks."
    )

    # Define optional flags
    parser.add_argument(
        "-t", "--tests", action="store_true", help="Run tests using pytest"
    )
    args = parser.parse_args()

    # Execute based on flags
    if args.tests:
        run_tests.main()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
