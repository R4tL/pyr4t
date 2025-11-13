"""CLI to generate python virtual environment."""

import argparse
from pyr4t.core import venv

def cmd_venv(args: argparse.Namespace):
    """
    Create a Python virtual environment.
    Args:
        args: Parsed command-line arguments.
    """

    venv(args.path)
    print(f"[info] Virtual environment created at: {args.path}")