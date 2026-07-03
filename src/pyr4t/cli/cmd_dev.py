"""CLI command for dev."""

import argparse

from pyr4t.core import ProjectArchM4nager


def cmd_dev(args: argparse.Namespace):
    """Initializes a new Python project using the provided arguments.

    Args:
        args (argparse.Namespace): parsed command-line arguments containing
            project details
    """

    pam = ProjectArchM4nager(proj_title=args.prj)
    pam.genretate_dev_env()


def add_dev_parser(subparsers: argparse._SubParsersAction):
    """Adds the 'dev' subcommand parser to the CLI.
    
    Args:
        subparsers (argparse._SubParsersAction): the subparsers object
            from the main parser
    """

    parser: argparse.ArgumentParser = subparsers.add_parser(
        "dev", help="Generate dev env in ./dev"
    )
    parser.add_argument(
        "--prj", "-p", default=None, help="Project title (default: current)"
    )
    parser.set_defaults(func=cmd_dev)
