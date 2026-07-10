"""CLI for deploying project with pip."""

import argparse

from pyr4t.core import ProjectCodeM4nager


def cmd_deploy(args: argparse.Namespace):
    """Deploy the specified project using pip.

    Args:
        args (argparse.Namespace): parsed command-line arguments containing
            project details
    """

    pcm = ProjectCodeM4nager(proj_title=args.prj)
    pcm.deploy(dev_mode=args.dev, python=args.python)


def add_deploy_parser(subparsers: argparse._SubParsersAction):
    """Adds the 'deploy' subcommand parser to the CLI.
    
    Args:
        subparsers (argparse._SubParsersAction): the subparsers object
            from the main parser
    """

    parser: argparse.ArgumentParser = subparsers.add_parser(
        "deploy", help="Deploy project with pip"
    )
    parser.add_argument(
        "--prj", "-p", default=None, help="Project title (default: current)"
    )
    parser.add_argument(
        "--dev", action="store_true", help="Deploy in dev and editable mode"
    )
    parser.add_argument(
        "--python",
        "-py",
        default=None,
        help="Specify the Python interpreter to use for deployment,"
         " works with any keyword (e.g., 'python3.13', 'python3', 'python',"
         " `'py -3.13'`) or an absolute path to the interpreter"
    )
    parser.set_defaults(func=cmd_deploy)
