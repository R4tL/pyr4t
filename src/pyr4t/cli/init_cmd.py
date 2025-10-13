"""CLI command for initializing a new Python project."""

import argparse

from pathlib import Path

from pyr4t.core import GenerateProject


def cmd_init(args: argparse.Namespace):
    """
    Initializes a new Python project using the provided arguments.
    Args:
        args (argparse.Namespace): Parsed command-line arguments containing project details.
    """

    """Function executed for 'init' command."""
    generator = GenerateProject(
        project_name=args.project_name,
        base_path=args.base_path,
        project_version=args.version,
        authors=args.authors,
    )
    generator.generate_project()
    print(f"[info] Project '{args.project_name}' initialized at {(Path(str(args.base_path)) / str(args.project_name)).resolve()}")


def add_init_parser(subparsers: argparse._SubParsersAction):
    """
    Adds the 'init' subcommand parser to the CLI.
    Args:
        subparsers (argparse._SubParsersAction): The subparsers object from the main parser.
    """

    """Add the 'init' subcommand parser."""
    parser: argparse.ArgumentParser = subparsers.add_parser(
        "init", help="Generate a new Python project structure"
    )

    parser.add_argument("project_name", type=str, help="The name of the project.")
    parser.add_argument(
        "-p",
        "--base_path",
        type=str,
        default=".",
        help="Base path where the project will be created.",
    )
    parser.add_argument(
        "-v",
        "--version",
        type=str,
        default="0.1.0",
        help="Initial project version (default: 0.1.0)",
    )
    parser.add_argument(
        "-a",
        "--authors",
        nargs="+",
        default=["me"],
        help='List of author aliases, e.g. --authors "alice" "bob"',
    )

    parser.set_defaults(func=cmd_init)
