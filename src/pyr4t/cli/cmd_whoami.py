"""CLI command for whoami."""

import argparse

from pyr4t.core import UserDBM4nager


def cmd_whoami(_: argparse.Namespace):
    """Initializes a new Python project using the provided arguments.

    Args:
        args (argparse.Namespace): parsed command-line arguments containing
           project details
    """

    dbu = UserDBM4nager()
    alias, user = dbu.whoami()
    print(f"  {alias}: {user.get('name', '')} <{user.get('email', '')}>")


def add_whoami_parser(subparsers: argparse._SubParsersAction):
    """Adds the 'whoami' subcommand parser to the CLI.
    
    Args:
        subparsers (argparse._SubParsersAction): the subparsers object
            from the main parser
    """

    parser: argparse.ArgumentParser = subparsers.add_parser(
        "whoami", help="Display the current default user"
    )
    parser.set_defaults(func=cmd_whoami)
