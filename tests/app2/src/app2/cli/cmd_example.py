"""CLI command for printing package version."""

import argparse


def cmd_example(args: argparse.Namespace):
    """
# TODO: update docstring
    Args:
        args:
    """

    """Print the current version of the package."""

    if args.action == "print":
        a = args.string
        if args.upper:
            a.upper()
        print(a)


def add_example_parser(subparsers: argparse._SubParsersAction):
    """
    Add the --version command to the CLI parser.
    Args:
        subparsers: The subparsers object from the main parser.
    """

    parser: argparse.ArgumentParser = subparsers.add_parser(
        "example", help="Example print cmd"
    )
    example_subparsers = parser.add_subparsers(dest="action", required=True)

    print_parser = example_subparsers.add_parser(
        "print", help="Print user inut"
    )
    print_parser.add_argument("string", help="string to print")
    print_parser.add_argument(
        "-u", "--upper", help="print in capital letters", action="store_true"
    )
    print_parser.set_defaults(func=cmd_example)