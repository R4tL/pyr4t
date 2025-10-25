"""CLI command for managing Pyr4t packages."""

import argparse

from pyr4t.core import (downgrade_pyr4tpackage, install_pyr4tpackage,
                        uninstall_pyr4tpackage, upgrade_pyr4tpackage)


def cmd_package(args: argparse.Namespace):
    """
    Installs a Pyr4t package using the provided arguments.
    Args:
        args (argparse.Namespace): Parsed command-line arguments.
    """

    match args.action:
        case "downgrade":
            downgrade_pyr4tpackage(args.package, args.version)
        case "install":
            install_pyr4tpackage(args.package, args.version)
        case "uninstall":
            uninstall_pyr4tpackage(args.package)
        case "upgrade":
            upgrade_pyr4tpackage(args.package, args.version)


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

    # ----- downgrade -----
    dwn_parser = package_subparsers.add_parser(
        "downgrade", help="Install a pyr4t package"
    )
    dwn_parser.add_argument("package", required=True, help="Package name")
    dwn_parser.add_argument("version", required=True, help="Package version")
    dwn_parser.set_defaults(func=cmd_package)

    # ----- install -----
    inst_parser = package_subparsers.add_parser(
        "install", help="Install a pyr4t package"
    )
    inst_parser.add_argument("package", required=True, help="Package name")
    inst_parser.add_argument(
        "-V", "--version", default="", help="Package version"
    )
    inst_parser.set_defaults(func=cmd_package)

    # ----- uninstall -----
    uninst_parser = package_subparsers.add_parser(
        "uninstall", help="Uninstall a pyr4t package"
    )
    uninst_parser.add_argument("package", required=True, help="Package name")
    uninst_parser.set_defaults(func=cmd_package)

    # ----- upgrade -----
    up_parser = package_subparsers.add_parser(
        "upgrade", help="Install a pyr4t package"
    )
    up_parser.add_argument("package", required=True, help="Package name")
    up_parser.add_argument(
        "-V", "--version", default="", help="Package version"
    )
    up_parser.set_defaults(func=cmd_package)