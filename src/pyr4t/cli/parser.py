"""Define the CLI argument parser for the Pyr4t project management tool."""

import argparse
import sys

from pyr4t import __version__
from .command_tree import get_tree
from .cmd_dev import add_dev_parser
from .cmd_package import add_package_parser
from .cmd_prod import add_prod_parser
from .cmd_proj import add_proj_parser
from .cmd_user import add_user_parser

def cmd_base(args: argparse.Namespace):
    """
# TODO: update docstring
    Args:
        args:
    """

    """
    Base commands in the root of CLI.

    """

    if args.help_requested:
        print(get_tree())
        print("")
        build_parser().print_help()
    elif args.version:
        print(f"Pyr4t {__version__}")
    elif args.command is None:
        print("[error] No command was entered. Use `-h` or `--help` for help.")
    sys.exit(0)



def build_parser():
    """
    Creates and configures the main argument parser for the Pyr4t CLI.
    Returns:
        argparse.ArgumentParser: The configured argument parser for
        the Pyr4t CLI.
    """

    parser = argparse.ArgumentParser(
        prog="pyr4t",
        description="CLI of the python manager pyr4t.", add_help=False
    )
    parser.add_argument(
    "-V", "--version", action = "store_true", help="Show version and exit"
    )
    parser.add_argument(
        "-h", "--help", action="store_true",
        dest="help_requested", help="Show help"
    )
    parser.set_defaults(func=cmd_base)
    subparsers = parser.add_subparsers(dest="command")

    add_dev_parser(subparsers)
    add_package_parser(subparsers)
    add_prod_parser(subparsers)
    add_proj_parser(subparsers)
    add_user_parser(subparsers)

    return parser