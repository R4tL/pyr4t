"""CLI command for managing Pyr4t packages."""

import argparse

from pyr4t.core import install_pyr4tpackage, uninstall_pyr4tpackage


def cmd_package(args: argparse.Namespace):
    """
    Installs a Pyr4t package using the provided arguments.
    Args:
        args (argparse.Namespace): Parsed command-line arguments.
    """

    match args.action:
        case "install":
            install_pyr4tpackage(args.package, args.version)
        case "uninstall":
            uninstall_pyr4tpackage(args.package)


def add_package_parser(subparsers: argparse._SubParsersAction):
    """
    Adds the 'install' command parser to the CLI.
    Args:
        subparsers (argparse._SubParsersAction): The subparsers object
        to which the parser will be added.
    """

    parser: argparse.ArgumentParser = subparsers.add_parser(
        "package", help="Manage Pyr4t packages"
    )
    package_subparsers = parser.add_subparsers(dest="action", required=True)

    # ----- install -----
    inst_parser = package_subparsers.add_parser(
        "install", help="Install a pyr4t package"
    )
    inst_parser.add_argument("package", help="Package name")
    inst_parser.add_argument(
        "-V", "--version", default="", help="Package version"
    )
    inst_parser.set_defaults(func=cmd_package)

    # ----- uninstall -----
    uninst_parser = package_subparsers.add_parser(
        "uninstall", help="Uninstall a pyr4t package"
    )
    uninst_parser.add_argument("package", help="Package name")
    uninst_parser.set_defaults(func=cmd_package)