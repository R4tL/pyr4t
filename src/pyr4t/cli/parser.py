"""
This module defines the CLI argument parser for the Pyr4t project management tool.
"""

import argparse
import sys

from .cmd_init import add_init_parser
from .cmd_install import add_install_parser
from .cmd_profile import add_profile_parser
from .cmd_help import cmd_help


def build_parser():
    """
    Creates and configures the main argument parser for the Pyr4t CLI.
    Returns:
        argparse.ArgumentParser: The configured argument parser for the Pyr4t CLI.
    """

    parser = argparse.ArgumentParser(
        prog="pyr4t", description="CLI of the python manager pyr4t."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    if "-h" in sys.argv or "--help" in sys.argv:
        print("\nCommand Tree:\n")
        cmd_help()
        print("\nHelp:\n")


    add_init_parser(subparsers)
    add_install_parser(subparsers)
    add_profile_parser(subparsers)

    return parser
