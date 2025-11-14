"""CLI for managing installation of pyr4t packages."""

import argparse

from pyr4t.core import install_pyr4tpackage, install_info


def cmd_install(args: argparse.Namespace) :
    """Install a pyr4t package.
    Args:
        args (argparse.pathspace): Parsed command-line arguments containing
        project details.
    """
    if args.info and args.package:
        raise ValueError("Cannot specify both --info and a package name.")
    if args.info:
        install_info()
    elif args.package:
        install_pyr4tpackage(args.package, args.version)
    else:
        raise ValueError("Either --info or a package name must be specified.")


def add_install_parser(subparsers: argparse._SubParsersAction):
    """
    Adds the 'install' subcommand parser to the CLI.
    Args:
        subparsers: The subparsers object from the main parser.
    """

    parser: argparse.ArgumentParser = subparsers.add_parser(
        "install", help="Install a pyr4t package"
    )
    parser.add_argument(
        "--info",
        action="store_true",
        help="Display information about the package without installing it",
    )
    parser.add_argument("package", nargs="?", help="Pyr4t package name")
    parser.add_argument(
        "-V", "--version", help="Specify the version of the package to install"
    )
    parser.set_defaults(func=cmd_install)
