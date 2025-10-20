"""
Main module for the project.
Provides the entry point for command-line interface operation.
"""

from pyr4t.cli import build_parser

def main():
    """Main entry point for the test20 CLI program."""
    parser = build_parser()
    args = parser.parse_args()

    if hasattr(args, "func"):
        args.func(args)
    else:
        print("Hello World")  # default comportement

if __name__ == "__main__":
    main()
