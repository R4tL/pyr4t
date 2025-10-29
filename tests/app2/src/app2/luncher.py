"""
Launcher module for the CLI.
Provides the entry point for running the application from the command line.
"""

from app2.__main__ import main as core_main


def main():
    """Runs the app2 application from the command line."""

    core_main()