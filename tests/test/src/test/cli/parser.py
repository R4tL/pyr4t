"""
Parser module for the CLI.
Creates the main argument parser and registers subcommands.
"""

from .cmd_version import add_version_parser


def build_parser():
    """Creates and configures the main argument parser for the CLI.
    Returns:
        argparse.ArgumentParser: The configured argument parser for the CLI.
    """

    parser = argparse.ArgumentParser(prog="test", description="CLI of test.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    add_version_parser(subparsers)

    return parser
