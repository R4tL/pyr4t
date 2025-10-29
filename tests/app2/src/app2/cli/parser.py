"""
Parser module for the CLI.
Creates the main argument parser and registers subcommands.
"""

import argparse
import sys

from app2 import __version__

from .cmd_example import add_example_parser
from .command_tree import get_tree


def cmd_base(args: argparse.Namespace):
    """
    Base commands in the root of CLI.
    Args:
        args (argparse.pathspace): Parsed command-line arguments containing
        project details.
    """

    if args.help_requested:
        print(get_tree())
        print("")
        build_parser().print_help()
    elif args.version:
        print(f"app2 {__version__}")
    elif args.command is None:
        print("[error] No command was entered. Use `-h` or `--help` for help.")
    sys.exit(0)


def build_parser():
    """Creates and configures the main argument parser for the CLI.
    Returns:
        argparse.ArgumentParser: The configured argument parser for the CLI.
    """

    parser = argparse.ArgumentParser(
        prog="app2", description="CLI of app2.", add_help=False
    )
    parser.add_argument(
        "-V", "--version", action="store_true", help="Show version and exit"
    )
    parser.add_argument(
        "-h",
        "--help",
        action="store_true",
        dest="help_requested",
        help="Show help",
    )
    parser.set_defaults(func=cmd_base)
    subparsers = parser.add_subparsers(dest="command")
    subparsers = parser.add_subparsers(dest="command")

    add_example_parser(subparsers)

    return parser