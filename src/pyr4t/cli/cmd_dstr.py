"""CLI for managing doc strings."""

import argparse

from pyr4t.core import ProjectCodeM4nager


def cmd_dstr(args: argparse.Namespace):
    """Generate or update docstrings for the specified project.

    Args:
        args (argparse.Namespace): parsed command-line arguments containing
            project details
    """

    pcm = ProjectCodeM4nager(proj_title=args.prj)
    pcm.dstr(specific=args.specific)


def add_dstr_parser(subparsers: argparse._SubParsersAction):
    """Adds the 'dstr' subcommand parser to the CLI.
    
    Args:
        subparsers (argparse._SubParsersAction): the subparsers object
            from the main parser
    """

    parser: argparse.ArgumentParser = subparsers.add_parser(
        "dstr", help="Generate or update docstrings"
    )
    parser.add_argument(
        "--prj", "-p", default=None, help="Project title (default: current)"
    )
    parser.add_argument(
        "specific",
        nargs="?",
        default="",
        help="Run specific test (dir or file or file::function)",
    )
    parser.set_defaults(func=cmd_dstr)
