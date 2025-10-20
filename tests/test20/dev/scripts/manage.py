"""
Development management CLI module.
Provides a CLI to format code and clean the project.
"""

import argparse
from . import format_code, clean


def main():
    """Main entry point for the development management CLI."""

    parser = argparse.ArgumentParser(
        description="Project utility CLI for common development tasks."
    )

    parser.add_argument("-f", "--format", action="store_true", help="Format code with black and isort")
    parser.add_argument(
        "-c", "--clean",
        nargs="?",
        const="cache",  
        choices=["all", "cache", "log", "tmp"],
        help="Clean files: 'all' (default), 'cache', 'log' (log files), or 'tmp' (files in /dev/tmp/)"
    )

    args = parser.parse_args()

    if args.format:
        format_code.main()
    elif args.clean:
        clean.main(args.clean)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
