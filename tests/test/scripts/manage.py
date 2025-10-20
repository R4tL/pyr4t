"""
Management CLI module.
Provides a command-line interface to run tests and other project management tasks.
"""

import argparse
from . import run_tests


def main():
    """Main entry point for the management CLI."""

    parser = argparse.ArgumentParser(
        description="Project utility CLI for common development tasks."
    )

    parser.add_argument("-t", "--tests", action="store_true", help="Run tests using pytest")
    args = parser.parse_args()

    if args.tests:
        run_tests.main()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
