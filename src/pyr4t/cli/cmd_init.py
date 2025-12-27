"""CLI for initializing project architecture."""

import argparse

from pyr4t.core import ProjectArchM4nager


def cmd_init(args: argparse.Namespace):
    """
    Initialize project architecture.
    Args:
        args (argparse.pathspace): Parsed command-line arguments containing
        project details.
    """

    pam = ProjectArchM4nager(
        proj_title=args.title,
        proj_base_path=args.path,
        authors=args.authors,
        proj_version=args.version,
    )
    if args.app:
        pam.generate_app_project()
    elif args.cli:
        pam.generate_cli_project()
    elif args.lib:
        pam.generate_lib_project()


def add_init_parser(subparsers: argparse._SubParsersAction):
    """
    Adds the 'init' subcommand parser to the CLI.
    Args:
        subparsers (argparse._SubParsersAction): The subparsers action to add
        the 'init' parser to.
    """

    parser: argparse.ArgumentParser = subparsers.add_parser(
        "init",
        help=(
            "Init a new python project creating a normalise package "
            "architecture"
        ),
    )
    group_init = parser.add_mutually_exclusive_group(required=True)
    group_init.add_argument(
        "--app", action="store_true", help="Application architecture"
    )
    group_init.add_argument(
        "--cli", action="store_true", help="CLI architecture"
    )
    group_init.add_argument(
        "--lib", action="store_true", help="Librairie architecture"
    )
    parser.add_argument("title", help="Project title")
    parser.add_argument(
        "-a",
        "--authors",
        nargs="+",
        default=["current"],
        help="List of authors",
    )
    parser.add_argument(
        "-p", "--path", default=".", help="Base path to create project"
    )
    parser.add_argument(
        "-V", "--version", default="0.1.0", help="Project version"
    )
    parser.set_defaults(func=cmd_init)
