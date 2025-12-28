"""CLI for running tests."""

import argparse

from pyr4t.core import ProjectCodeM4nager


def cmd_test(args: argparse.Namespace):
    """
    Run tests for the specified project.
    Args:
        args (argparse.Namespace): parsed command-line arguments containing
            project details
    """

    pcm = ProjectCodeM4nager(proj_title=args.prj)
    pcm.test(specific=args.specific)


def add_test_parser(subparsers: argparse._SubParsersAction):
    """
    Adds the 'test' subcommand parser to the CLI.
    Args:
        subparsers (argparse._SubParsersAction): the subparsers object
            from the main parser
    """

    parser: argparse.ArgumentParser = subparsers.add_parser(
        "test", help="Run tests"
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
    parser.set_defaults(func=cmd_test)
