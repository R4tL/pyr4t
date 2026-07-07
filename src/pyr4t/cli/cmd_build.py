"""CLI for building binary for project."""

import argparse

from pyr4t.core import ProjectCodeM4nager


def cmd_build(args: argparse.Namespace):
    """Build binary for the specified project.

    Args:
        args (argparse.Namespace): parsed command-line arguments containing
            project details
    """

    pcm = ProjectCodeM4nager(proj_title=args.prj)
    pcm.build()


def add_build_parser(subparsers: argparse._SubParsersAction):
    """Adds the 'build' subcommand parser to the CLI.
    
    Args:
        subparsers (argparse._SubParsersAction): the subparsers object
            from the main parser
    """

    parser: argparse.ArgumentParser = subparsers.add_parser(
        "build", help="Build binary for project"
    )
    parser.add_argument(
        "--prj", "-p", default=None, help="Project title (default: current)"
    )
    parser.set_defaults(func=cmd_build)
