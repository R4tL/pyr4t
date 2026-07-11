"""CLI for running scripts."""

import argparse

from pyr4t.core import ProjectCodeM4nager


def cmd_run(args: argparse.Namespace):
    """Run scripts for the specified project.

    Args:
        args (argparse.Namespace): parsed command-line arguments containing
            project details
    """

    pcm = ProjectCodeM4nager(proj_title=args.prj)
    pcm.run(
        script=args.script,
        dev_mode=args.dev,
        python=args.python,
        args=args.script_args,
    )


def add_run_parser(subparsers: argparse._SubParsersAction):
    """Adds the 'run' subcommand parser to the CLI.
    
    Args:
        subparsers (argparse._SubParsersAction): the subparsers object
            from the main parser
    """

    parser: argparse.ArgumentParser = subparsers.add_parser(
        "run", help="Run script files stored in ./scripts"
    )
    parser.add_argument(
        "--prj", "-p", default=None, help="Project title (default: current)"
    )
    parser.add_argument(
        "--dev", action="store_true", help="Dev script stored in ./dev/scripts"
    )
    parser.add_argument("script", help="Script name")
    parser.add_argument(
        "script_args",
        nargs=argparse.REMAINDER,
        help="Arguments passed to the script",
    )
    parser.add_argument(
        "--python",
        "-py",
        default=None,
        help="Specify the Python interpreter to use for running scripts,"
        " works with any keyword (e.g., 'python3.13', 'python3', 'python',"
        " `'py -3.13'`) or an absolute path to the interpreter"
        "(default: active venv/python)"
    )
    parser.set_defaults(func=cmd_run)
