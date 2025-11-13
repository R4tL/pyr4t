"""CLI for formating code."""

import argparse

from pyr4t.core import ProjectCodeM4nager


def cmd_fmt(args: argparse.Namespace):
    """
    Format source code for the specified project.
    Args:
        args (argparse.pathspace): Parsed command-line arguments containing
        project details.
    """

    pcm = ProjectCodeM4nager(proj_title=args.prj)
    pcm.fmt()


def add_fmt_parser(subparsers: argparse._SubParsersAction):
    """
    Adds the 'fmt' subcommand parser to the CLI.
    Args:
        subparsers: The subparsers object from the main parser.
    """

    parser: argparse.ArgumentParser = subparsers.add_parser(
        "fmt", help="Format source code"
    )
    parser.add_argument(
        "--prj", "-p", default=None, help="Project title (default: current)"
    )
    parser.set_defaults(func=cmd_fmt)
