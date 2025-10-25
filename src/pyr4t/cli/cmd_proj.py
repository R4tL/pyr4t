"""CLI command for managing Pyr4t projects."""

import argparse

from pyr4t.core import ProjectArchM4nager, ProjectDBM4nager


def cmd_proj(args: argparse.Namespace):
    """
    Initializes a new Python project using the provided arguments.
    Args:
        args (argparse.pathspace): Parsed command-line arguments containing
        project details.
    """

    if args.action == "init":
        amgr = ProjectArchM4nager(
            args.title, args.path, args.authors, args.version
        )
        if args.app:
            amgr.generate_app_project()
        elif args.cli:
            amgr.generate_cli_project()
        elif args.lib:
            amgr.generate_lib_project()

    else:
        dbp = ProjectDBM4nager()
        match args.action:

            case "add":
                dbp.add(args.title, args.path, args.version)
                print(f"[info] Project added: {args.title}: {args.path}")

            case "list":
                projects = dbp.list()
                if not projects:
                    print("[warning] No projects found.")
                else:
                    for title, project in projects.items():
                        print(f"[info] {title}: {project.get("path", "")}")

            case "modify":
                dbp.modify(args.title, path=args.path, version=args.version)
                if args.path or args.version:
                    print(f"Project updated: {args.title}")

            case "rm":
                dbp.remove(args.title)
                print(f"[info] Project removed: {args.title}")

            case "swicth":
                dbp.switch(args.title)
                print(f"[info] Default project selected: {args.title}")

            case "whoami":
                title, project = dbp.whoami()
                print(f"[info] {title}: {project.get("path", "")}")


def add_proj_parser(subparsers: argparse._SubParsersAction):
    """
    Adds the 'proj' subcommand parser to the CLI.
    Args:
        subparsers: The subparsers object from the main parser.
    """

    parser: argparse.ArgumentParser = subparsers.add_parser(
        "proj", help="Manage a pyr4t project"
    )

    proj_subparsers = parser.add_subparsers(dest="action", required=True)

    # ----- add -----
    add_parser = proj_subparsers.add_parser("add", help="Add a new project")
    add_parser.add_argument("title",  help="Project title")
    add_parser.add_argument("path",  help="Project path")
    add_parser.add_argument("version",  help="Project version")
    add_parser.set_defaults(func=cmd_proj)

    # ----- init -----
    init_parser = proj_subparsers.add_parser(
        "init",
        help=(
            "Init a new python project creating a normalise package "
            "architecture"
        ),
    )
    group_init = init_parser.add_mutually_exclusive_group(required=True)
    group_init.add_argument(
        "--app", action="store_true", help="Application architecture"
    )
    group_init.add_argument(
        "--cli", action="store_true", help="CLI architecture"
    )
    group_init.add_argument(
        "--lib", action="store_true", help="Librairie architecture"
    )
    init_parser.add_argument("title",  help="Project title")
    init_parser.add_argument(
        "-a",
        "--authors",
        nargs="+",
        default=["current"],
        help="List of authors",
    )
    init_parser.add_argument(
        "-p", "--path", default=".", help="Base path to create project"
    )
    init_parser.add_argument(
        "-V", "--version", default="0.1.0", help="Project version"
    )
    init_parser.set_defaults(func=cmd_proj)

    # ----- list -----
    list_parser = proj_subparsers.add_parser("list", help="List projects")
    list_parser.set_defaults(func=cmd_proj)

    # ----- modify -----
    modify_parser = proj_subparsers.add_parser(
        "modify", help="Modify a project"
    )
    modify_parser.add_argument("title",  help="Project title")
    modify_parser.add_argument("-p", "--path", help="New project path")
    modify_parser.add_argument("-V", "--version", help="New project verrsion")
    modify_parser.set_defaults(func=cmd_proj)

    # ----- switch -----
    select_parser = proj_subparsers.add_parser(
        "switch", help="Switch current project"
    )
    select_parser.add_argument("title",  help="Project title")
    select_parser.set_defaults(func=cmd_proj)

    # ----- remove -----
    remove_parser = proj_subparsers.add_parser("rm", help="Remove a project")
    remove_parser.add_argument("title",  help="Project title")
    remove_parser.set_defaults(func=cmd_proj)

    # ----- whoami -----
    whoami_parser = proj_subparsers.add_parser(
        "whoami", help="Show the current project"
    )
    whoami_parser.set_defaults(func=cmd_proj)
