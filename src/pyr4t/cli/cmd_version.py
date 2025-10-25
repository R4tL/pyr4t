"""CLI command for printing package version."""

import argparse

from pyr4t import __version__


def cmd_version():
    """Print the current version of the package."""

    print(f"Pyr4t {__version__}")


def add_version_parser(subparsers: argparse._SubParsersAction):
    """
    Add the --version command to the CLI parser.
        Args:
            subparsers: The subparsers object from the main parser.
    """

    parser: argparse.ArgumentParser = subparsers.add_parser(
        "-V", "--version", help="Print the version of package test2"
    )
    parser.set_defaults(func=cmd_version)
