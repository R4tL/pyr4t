import argparse
from . import format_code, clean
from pyr4t.main import main as run_main

def main():
    parser = argparse.ArgumentParser(
        description="Project utility CLI for common development tasks."
    )

    # Define optional flags
    parser.add_argument("-r", "--run", action="store_true", help="Run the main project script with args")
    parser.add_argument("-f", "--format", action="store_true", help="Format code with black and isort")
    parser.add_argument(
    "-c", "--clean",
    nargs="?",
    const="cache",  # Default if no value provided
    choices=["all", "cache", "log", "tmp"],
    help="Clean files: 'all' (default), 'cache', 'log' (log files), or 'tmp' (files in /dev/tmp/)"
    )

    args = parser.parse_args()

    # Execute based on flags
    if args.run:
        run_main(args.run)
    elif args.format:
        format_code.main()
    elif args.clean:
        clean.main(args.clean)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
