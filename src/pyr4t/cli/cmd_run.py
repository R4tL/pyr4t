"""CLI for running scripts."""

import argparse

from pyr4t.core import ProjectCodeM4nager


def cmd_run(args: argparse.Namespace):
    """
    Run scripts for the specified project.
    Args:
        args (argparse.pathspace): Parsed command-line arguments containing
        project details.
    """

    pcm = ProjectCodeM4nager(proj_title=args.prj)
    pcm.run(script=args.script, dev_mode=args.dev)


def add_run_parser(subparsers: argparse._SubParsersAction):
    """
    Adds the 'run' subcommand parser to the CLI.
    Args:
        subparsers: The subparsers object from the main parser.
    """

    parser: argparse.ArgumentParser = subparsers.add_parser(
        "run", help="Run scripts"
    )
    parser.add_argument(
        "--prj", "-p", default=None, help="Project title (default: current)"
    )
    parser.add_argument(
        "--dev", action="store_true", help="Dev script"
    )
    parser.add_argument(
        "script", default="main", nargs="?", help="Script name (default: main)"
    )
    parser.set_defaults(func=cmd_run)
