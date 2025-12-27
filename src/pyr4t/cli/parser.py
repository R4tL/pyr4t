"""Define the CLI argument parser for the Pyr4t project management tool."""

import argparse
import sys

from pyr4t import __version__

from .cmd_build import add_build_parser
from .cmd_cls import add_cls_parser
from .cmd_deploy import add_deploy_parser
from .cmd_dev import add_dev_parser
from .cmd_dstr import add_dstr_parser
from .cmd_fmt import add_fmt_parser
from .cmd_info import add_info_parser
from .cmd_init import add_init_parser
from .cmd_install import add_install_parser
from .cmd_prj import add_prj_parser
from .cmd_run import add_run_parser
from .cmd_test import add_test_parser
from .cmd_usr import add_usr_parser
from .cmd_venv import add_venv_parser
from .cmd_whoami import add_whoami_parser
from .command_tree import get_tree


def cmd_base(args: argparse.Namespace):
    """
    Handle base CLI actions.
    Args:
        args (argparse.pathspace): Parsed command-line arguments containing
        project details.
    """

    if args.help_requested:
        print(get_tree())
        print("")
        build_parser().print_help()
    elif args.version:
        print(f"Pyr4t {__version__}")
    elif args.command is None:
        print("[error] No command was entered. Use `-h` or `--help` for help.")
    sys.exit(0)


def build_parser() -> argparse.ArgumentParser:
    """
    Creates and configures the main argument parser for the Pyr4t CLI.
    Returns:
        argparse.ArgumentParser: The configured argument parser for
        the Pyr4t CLI.
    """

    parser = argparse.ArgumentParser(
        prog="pyr4t",
        description="CLI of the python manager pyr4t.",
        add_help=False,
    )
    parser.add_argument(
        "-V", "--version", action="store_true", help="Show version and exit"
    )
    parser.add_argument(
        "-h",
        "--help",
        action="store_true",
        dest="help_requested",
        help="Show help and exit",
    )
    parser.set_defaults(func=cmd_base)
    subparsers = parser.add_subparsers(dest="command")

    add_build_parser(subparsers)
    add_cls_parser(subparsers)
    add_deploy_parser(subparsers)
    add_dev_parser(subparsers)
    add_dstr_parser(subparsers)
    add_fmt_parser(subparsers)
    add_info_parser(subparsers)
    add_init_parser(subparsers)
    add_install_parser(subparsers)
    add_prj_parser(subparsers)
    add_run_parser(subparsers)
    add_test_parser(subparsers)
    add_usr_parser(subparsers)
    add_venv_parser(subparsers)
    add_whoami_parser(subparsers)

    return parser
