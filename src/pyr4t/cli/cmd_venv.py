"""CLI for generating python project architecture."""

import argparse

from pyr4t.core import ProjectCodeM4nager


def cmd_venv(args: argparse.Namespace):
    """Create a Python virtual environment.

    Args:
        args (argparse.pathspace): parsed command-line arguments containing
           project details
    """

    pcm = ProjectCodeM4nager(proj_title=args.prj)
    pcm.venv(python=args.python)


def add_venv_parser(subparsers: argparse._SubParsersAction):
    """Adds the 'venv' subcommand parser to the CLI.
    
    Args:
        subparsers (argparse._SubParsersAction): the subparsers object
            from the main parser
    """

    parser: argparse.ArgumentParser = subparsers.add_parser(
        "venv", help="Create a Python virtual environment in ./.venv"
    )
    parser.add_argument(
        "--prj", "-p", default=None, help="Project title (default: current)"
    )
    parser.add_argument(
        "--python",
        "-py",
        default=None,
        help="Python interpreter to use (default: active venv/python)",
    )
    parser.set_defaults(func=cmd_venv)
