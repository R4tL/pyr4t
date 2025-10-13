"""
This module defines the CLI argument parser for the Pyr4t project management tool.
"""

import argparse

from .cmd_init import add_init_parser
from .cmd_install import add_install_parser
from .cmd_profile import add_profile_parser


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

    add_init_parser(subparsers)
    add_install_parser(subparsers)
    add_profile_parser(subparsers)

    return parser