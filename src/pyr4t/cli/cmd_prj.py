"""CLI command for managing Pyr4t projects."""

import argparse
import shutil
from pathlib import Path

from pyr4t.core import ProjectDBM4nager
from pyr4t.exceptions import Pyr4tValueError


def cmd_prj(args: argparse.Namespace):
    """Initializes a new Python project using the provided arguments.

    Args:
        args (argparse.Namespace): parsed command-line arguments containing
            project details

    Raises:
        Pyr4tValueError: If required arguments are missing or invalid.
    """

    dbp = ProjectDBM4nager()
    match args.action:

        case "add":
            path = str(Path(args.path).resolve())
            dbp.add(args.title, path, args.version)

        case "ls":
            projects = dbp.list()
            if not projects:
                print("[warning] No projects found.")
            else:
                for title, project in projects.items():
                    if title == dbp.current:
                        print(
                            f"* {title}: {project.get("path", "")} "
                            f"<{project.get("version", "")}>"
                        )
                    else:
                        print(
                            f"  {title}: {project.get("path", "")} "
                            f"<{project.get("version", "")}>"
                        )

        case "mv":
            if not args.path and not args.version:
                raise Pyr4tValueError(
                    "Either --path or --version must be specified."
                )
            path = Path(args.path).resolve() if args.path else None
            dbp.modify(args.title, path=path, version=args.version)

        case "rm":
            if args.files:
                print(
                    "[warning] Do you want to delete the files for "
                    f"project {args.title}? (y/n)"
                )
                response = input().lower()
                if response == "y":
                    print(
                        f"[info] Deleting project files for: {args.title}..."
                    )
                    path = dbp.listd.get(args.title, {}).get("path", {})
                    dbp.remove(args.title)
                    shutil.rmtree(path, ignore_errors=True)
                else:
                    print("[info] Project files not deleted.")
            else:
                dbp.remove(args.title)

        case "switch":
            dbp.switch(args.title)




def add_prj_parser(subparsers: argparse._SubParsersAction):
    """Adds the 'prj' subcommand parser to the CLI.
    
    Args:
        subparsers (argparse._SubParsersAction): the subparsers object
            from the main parser
    """

    parser: argparse.ArgumentParser = subparsers.add_parser(
        "prj", help="Manage a pyr4t project"
    )

    proj_subparsers = parser.add_subparsers(dest="action", required=True)

    # ----- add -----
    add_parser = proj_subparsers.add_parser("add", help="Add a new project")
    add_parser.add_argument("title", help="Project title")
    add_parser.add_argument("path", help="Project path")
    add_parser.add_argument("version", help="Project version")
    add_parser.set_defaults(func=cmd_prj)

    # ----- ls -----
    list_parser = proj_subparsers.add_parser("ls", help="List projects")
    list_parser.set_defaults(func=cmd_prj)

    # ----- mv -----
    modify_parser = proj_subparsers.add_parser("mv", help="Modify a project")
    modify_parser.add_argument("title", help="Project title")
    modify_parser.add_argument("-p", "--path", help="New project path")
    modify_parser.add_argument("-V", "--version", help="New project verrsion")
    modify_parser.set_defaults(func=cmd_prj)

    # ----- switch -----
    select_parser = proj_subparsers.add_parser(
        "switch", help="Switch current project"
    )
    select_parser.add_argument("title", help="Project title")
    select_parser.set_defaults(func=cmd_prj)

    # ----- rm -----
    remove_parser = proj_subparsers.add_parser("rm", help="Remove a project")
    remove_parser.add_argument("title", help="Project title")
    remove_parser.add_argument(
        "-f", "--files", action="store_true", help="Delete project files too"
    )
    remove_parser.set_defaults(func=cmd_prj)
