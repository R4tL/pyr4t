"""CLI command for doc."""

import argparse

from pyr4t.core import ProjectArchM4nager


def cmd_doc(args: argparse.Namespace):
    """Initializes Sphynx documentation files for the project.

    Args:
        args (argparse.Namespace): parsed command-line arguments containing
            project details
    """

    pam = ProjectArchM4nager(proj_title=args.prj)
    pam.generate_docs_files()


def add_doc_parser(subparsers: argparse._SubParsersAction):
    """Adds the 'doc' subcommand parser to the CLI.

    Args:
        subparsers (argparse._SubParsersAction): the subparsers object
            from the main parser
    """

    parser: argparse.ArgumentParser = subparsers.add_parser(
        "doc", help="Generate input documentation files for Sphinx"
    )
    parser.add_argument(
        "--prj", "-p", default=None, help="Project title (default: current)"
    )
    parser.set_defaults(func=cmd_doc)
