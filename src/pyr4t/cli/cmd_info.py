"""CLI command for info."""

import argparse

from pyr4t.core import ProjectDBM4nager


def cmd_info(_: argparse.Namespace):
    """Initializes a new Python project using the provided arguments.

    Args:
        args (argparse.Namespace): parsed command-line arguments containing
           project details
    """

    dbp = ProjectDBM4nager()
    title, prj = dbp.info()
    print(f"  {title}: {prj.get('path', '')} <{prj.get('version', '')}>")


def add_info_parser(subparsers: argparse._SubParsersAction):
    """Adds the 'info' subcommand parser to the CLI.
    
    Args:
        subparsers (argparse._SubParsersAction): the subparsers object
            from the main parser
    """

    parser: argparse.ArgumentParser = subparsers.add_parser(
        "info", help="Display the current default user"
    )
    parser.set_defaults(func=cmd_info)
