"""
Main module for the Pyr4t CLI.
Provides the entry point for command-line interface operations.
"""

import argparse

from pyr4t.cli.init_cmd import add_init_parser
from pyr4t.cli.install_cmd import add_install_parser
from pyr4t.cli.profile_cmd import add_profile_parser


def main():
    """Main entry point for the Pyr4t CLI program."""

    parser = argparse.ArgumentParser(
        prog="pyr4t", description="CLI de gestion de projets Pyr4t"
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Enregistre toutes les sous-commandes
    add_init_parser(subparsers)
    add_install_parser(subparsers)
    add_profile_parser(subparsers)

    # Parse et exécute
    args = parser.parse_args()
    args.func(args)
