"""CLI for managing doc strings."""

import argparse

from pyr4t.core import ProjectCodeM4nager


def cmd_dstr(args: argparse.Namespace):
    """
    Generate or update docstrings for the specified project.
    Args:
        args (argparse.pathspace): Parsed command-line arguments containing
        project details.
    """

    pcm = ProjectCodeM4nager(proj_title=args.prj)
    pcm.dstr()


def add_dstr_parser(subparsers: argparse._SubParsersAction):
    """
    Adds the 'dstr' subcommand parser to the CLI.
    Args:
        subparsers: The subparsers object from the main parser.
    """

    parser: argparse.ArgumentParser = subparsers.add_parser(
        "dstr", help="Generate or update docstrings"
    )
    parser.add_argument(
        "--prj", "-p", default=None, help="Project title (default: current)"
    )
    parser.set_defaults(func=cmd_dstr)
