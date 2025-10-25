"""CLI command for dev."""

import argparse

from pyr4t.core import dev_deploy, dev_run, cls, dstr, fmt, init

def cmd_dev(args: argparse.Namespace):
    """
    Dev commands for current project.
    Args:
        args (argparse.pathspace): Parsed command-line arguments containing
        project details.
    """

    match args.action:
        case "deploy":
            dev_deploy()
        case "run":
            dev_run(args.scipt)
        case "cls":
            cls([args.cache, args.log, args.tmp])
        case "dstr":
            dstr(args.specific)
        case "fmt":
            fmt(args.specific)
        case "init":
            init()

def add_dev_parser(subparsers: argparse._SubParsersAction):
    """
    Adds the 'dev' subcommand parser to the CLI.
    Args:
        subparsers: The subparsers object from the main parser.
    """

    parser: argparse.ArgumentParser = subparsers.add_parser(
        "dev", help="Commands in dev mode"
    )

    dev_subparsers = parser.add_subparsers(dest="action", required=True)


    # ----- deploy -----
    dep_parser = dev_subparsers.add_parser(
        "deploy", help="Deploy project using pip"
    )
    dep_parser.set_defaults(func=cmd_dev)

    # ----- run -----
    run_parser = dev_subparsers.add_parser(
        "run", help="Run a script from /script dir"
    )
    run_parser.add_argument(
        "script", default="main", nargs="?", help="Script name (default: main)"
    )
    run_parser.set_defaults(func=cmd_dev)

    # ----- init -----
    init_parser = dev_subparsers.add_parser(
        "init", help="Init a dev env in /dev dir"
    )
    init_parser.set_defaults(func=cmd_dev)

    # ----- cls -----
    cls_parser = dev_subparsers.add_parser(
        "cls", help="Clean files (default: all)"
    )
    cls_parser.add_argument(
        "--cache", action="store_const", const="cache",
        default=None, help="Clean cache"
    )
    cls_parser.add_argument(
        "--log", action="store_const", const="log",
        default=None, help="Clean logs"
    )
    cls_parser.add_argument(
        "--tmp", action="store_const", const="tmp",
        default=None, help="Clean tmp"
    )
    cls_parser.set_defaults(func=cmd_dev)

    # ----- fmt -----
    fmt_parser = dev_subparsers.add_parser("fmt", help="Format code")
    fmt_parser.add_argument("specific", help="Specific file(s) (dir or file)")
    fmt_parser.set_defaults(func=cmd_dev)

    # ----- dstr -----
    dstr_parser = dev_subparsers.add_parser("dstr", help="Analyse docstrings")
    dstr_parser.add_argument("specific", help="Specific file(s) (dir or file)")
    dstr_parser.set_defaults(func=cmd_dev)
