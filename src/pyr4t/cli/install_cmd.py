"""
CLI command for installing Pyr4t packages.
This module provides the 'install' command for the Pyr4t CLI, allowing users to install packages from GitHub using specified protocols and versions.
"""

import argparse

from pyr4t.core import pyr4t_install


def cmd_install(args: argparse.Namespace):
    """
    Installs a Pyr4t package using the provided arguments.
    Args:
        args (argparse.Namespace): Parsed command-line arguments containing
            - name (str): Name of the Pyr4t package to install.
            - version (str): Version of the package to install.
            - protocol (str): Protocol to use for installation (https or ssh).
    """

    pyr4t_install(args.name, version=args.version, protocol=args.protocol)
    print(f"[info] Installed Pyr4t package: {args.name} (version: {args.version})")


def add_install_parser(subparsers: argparse._SubParsersAction):
    """
    Adds the 'install' command parser to the CLI.
    Args:
        subparsers (argparse._SubParsersAction): The subparsers object to which the 'install' parser will be added.
    """

    parser: argparse.ArgumentParser = subparsers.add_parser(
        "install", help="Install a Pyr4t package from GitHub"
    )
    parser.add_argument("name", type=str, help="Name of the Pyr4t package")
    parser.add_argument(
        "-v", "--version", type=str, default="main", help='Version (default: "main")'
    )
    parser.add_argument(
        "-p",
        "--protocol",
        type=str,
        default="https",
        choices=["https", "ssh"],
        help="Protocol",
    )
    parser.set_defaults(func=cmd_install)
