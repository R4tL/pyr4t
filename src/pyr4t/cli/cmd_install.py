"""CLI for managing installation of pyr4t packages."""

import argparse

from pyr4t.core import install_pyr4tpackage, install_info, maj_token


def cmd_install(args: argparse.Namespace) :
    """Install a pyr4t package.
    Args:
        args (argparse.pathspace): Parsed command-line arguments containing
        project details.
    """

    if args.token:
        maj_token(args.token)
    if args.package:
        install_pyr4tpackage(args.package, args.version)
    if args.info:
        install_info(show_private=False)
    if args.info_private:
        install_info(show_private=True)
    if not (args.package or args.info or args.info_private or args.token):
        print("[error] No action specified. Use `-h` or `--help` for help.")


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
        help="Display package info"
    )
    parser.add_argument(
        "--info-private",
        action="store_true",
        help="Display package info including private packages"
    )
    parser.add_argument(
        "--token", help="Update the GitHub token for private pyr4t packages"
    )
    parser.add_argument("package", nargs="?", help="Pyr4t package name")
    parser.add_argument(
        "-V", "--version", help="Specify the version of the package to install"
    )
    parser.set_defaults(func=cmd_install)
