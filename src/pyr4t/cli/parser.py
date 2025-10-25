"""Define the CLI argument parser for the Pyr4t project management tool."""

import argparse
import sys

from .cmd_help import cmd_help
from .cmd_package import add_package_parser
from .cmd_prod import add_prod_parser
from .cmd_proj import add_proj_parser
from .cmd_user import add_user_parser


def build_parser():
    """
    Creates and configures the main argument parser for the Pyr4t CLI.
    Returns:
        argparse.ArgumentParser: The configured argument parser for
        the Pyr4t CLI.
    """

    parser = argparse.ArgumentParser(
        prog="pyr4t", description="CLI of the python manager pyr4t."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    if "-h" in sys.argv or "--help" in sys.argv:
        print("\nCommand Tree:\n")
        cmd_help()
        print("\nHelp:\n")

    add_package_parser(subparsers)
    add_prod_parser(subparsers)
    add_proj_parser(subparsers)
    add_user_parser(subparsers)

    return parser
