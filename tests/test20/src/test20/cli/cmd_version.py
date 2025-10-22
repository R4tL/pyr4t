"""
Version command for the CLI.
Provides a parser for the --version option.
"""

import argparse

from pyr4t import __version__


def cmd_version(args: argparse.Namespace):
    """Print the current version of the package."""

    print(__version__)


def add_version_parser(subparsers: argparse._SubParsersAction):
    """Add the --version command to the CLI parser."""

    parser: argparse.ArgumentParser = subparsers.add_parser(
        "--version", help="Print the version of package test20"
    )
    parser.set_defaults(func=cmd_version)
