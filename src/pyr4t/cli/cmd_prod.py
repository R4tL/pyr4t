"""CLI command for prod."""

import argparse

from pyr4t.core import build, deploy, run, test

def cmd_prod(args: argparse.Namespace):
    """
    Prod commands for current project.
    Args:
        args (argparse.pathspace): Parsed command-line arguments containing
        project details.
    """

    match args.action:
        case "build":
            build()
        case "deploy":
            deploy()
        case "run":
            run(args.scipt)
        case "test":
            test(args.sepcific)

def add_prod_parser(subparsers: argparse._SubParsersAction):
    """
    Adds the 'prod' subcommand parser to the CLI.
    Args:
        subparsers: The subparsers object from the main parser.
    """

    parser: argparse.ArgumentParser = subparsers.add_parser(
        "prod", help="Commands in prod mode"
    )

    prod_subparsers = parser.add_subparsers(dest="action", required=True)


    # ----- build -----
    build_parser = prod_subparsers.add_parser(
        "build", help="Build a binary file of the project"
    )
    build_parser.set_defaults(func=cmd_prod)

    # ----- deploy -----
    dep_parser = prod_subparsers.add_parser(
        "deploy", help="Deploy project using pip"
    )
    dep_parser.set_defaults(func=cmd_prod)

    # ----- run -----
    run_parser = prod_subparsers.add_parser(
        "run", help="Run a script from /script dir"
    )
    run_parser.add_argument(
        "script", default="main", nargs="?", help="Script name (default: main)"
    )
    run_parser.set_defaults(func=cmd_prod)

    # ----- test -----
    test_parser = prod_subparsers.add_parser(
        "test", help="Run tests from /test dir"
    )
    test_parser.add_argument(
        "specific", default="",
        help="Run specific test (dir or file or file::function)"
    )
    test_parser.set_defaults(func=cmd_prod)
