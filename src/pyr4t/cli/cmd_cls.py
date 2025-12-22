"""CLI for clearing files."""

import argparse

from pyr4t.core import ProjectCodeM4nager


def cmd_cls(args: argparse.Namespace):
    """
    Clear temporary and build files for the specified project.
    Args:
        args (argparse.pathspace): Parsed command-line arguments containing
        project details.
    """

    pcm = ProjectCodeM4nager(proj_title=args.prj)
    pcm.cls()


def add_cls_parser(subparsers: argparse._SubParsersAction):
    """
    Adds the 'cls' subcommand parser to the CLI.
    Args:
        subparsers: The subparsers object from the main parser.
    """

    parser: argparse.ArgumentParser = subparsers.add_parser(
        "cls", help="Clear tmp/cache/log files"
    )
    parser.add_argument(
        "--prj", "-p", default=None, help="Project title (default: current)"
    )
    parser.add_argument(
        "--cache", action="store_const", const="cache",
        default=None, help="Clean cache"
    )
    parser.add_argument(
        "--log", action="store_const", const="log",
        default=None, help="Clean logs"
    )
    parser.add_argument(
        "--tmp", action="store_const", const="tmp",
        default=None, help="Clean tmp"
    )
    parser.set_defaults(func=cmd_cls)
