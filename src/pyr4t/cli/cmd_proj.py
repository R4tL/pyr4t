"""CLI command for initializing a new Python project."""

import argparse

from pyr4t.core import ProjectArchM4nager, ProjectDBM4nager


def cmd_proj(args: ):
    """
    Initializes a new Python project using the provided arguments.
    Args:
        args (argparse.pathspace): Parsed command-line arguments containing project details.
    """

    if args.action == "init":
        ...



    else:
        dbmgr = ProjectDBM4nager()
        match args.action:

            case "add":
                dbmgr.add(args.title, path=args.path)
                print(
                    f"[info] Profile added: {args.title}: {args.path}"
                )

            case "list":
                profiles = dbmgr.list()
                if not profiles:
                    print("[warning] No profiles found.")
                else:
                    for title, profile in profiles.items():
                        print(
                            f"[info] {title}: {profile.get("path", "")}"
                        )

            case "modify":
                dbmgr.modify(args.title, path=args.path)
                print(f"Profile updated: {args.title}")

            case "rm":
                dbmgr.remove(args.title)
                print(f"[info] Profile removed: {args.title}")

            case "swicth":
                dbmgr.switch(args.title)
                print(f"[info] Default profile selected: {args.title}")

            case "whoami":
                title, profile = dbmgr.whoami()
                print(
                    f"[info] {title}: {profile.get("path", "")} "
                    f"<{profile.get("email", "")}>"
                )



def add_init_parser(subparsers: argparse._SubParsersAction):
    """
    Adds the 'init' subcommand parser to the CLI.
    Args:
        subparsers: The subparsers object from the main parser.
    """

    parser: argparse.ArgumentParser = subparsers.add_parser(
        "proj", help="Generate a new Python project structure"
    )

    proj_subparsers = parser.add_subparsers(dest="action", required=True)

    # ----- add -----
    add_parser = proj_subparsers.add_parser("add", help="Add a new project")
    add_parser.add_argument("title", required=True, help="Project title")
    add_parser.add_argument("path", required=True, help="Project path")
    add_parser.set_defaults(func=cmd_proj)

    # ----- init -----
    init_parser = proj_subparsers.add_parser(
        "init", 
        help=(
        "Init a new python project creating a normalise package "
        "architecture"
        )
    )
    init_parser.add_argument(
        "--app", action="store_true", help="Application architecture"
    )
    init_parser.add_argument(
        "--cli", action="store_true", help="CLI architecture"
    )
    init_parser.add_argument(
        "--lib", action="store_true", help="Librairie architecture"
    )
    init_parser.add_argument("title", required=True, help="Project title")
    init_parser.add_argument(
        "-a", "--authors",
        nargs="+",
        default=["current"],
        help="List of authors"
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
    modify_parser.add_argument("title", required=True, help="Project title")
    modify_parser.add_argument("path", help="New project path")
    modify_parser.set_defaults(func=cmd_proj)

    # ----- switch -----
    select_parser = proj_subparsers.add_parser(
        "switch", help="Switch current project"
    )
    select_parser.add_argument(
        "title", required=True, help="Project title"
    )
    select_parser.set_defaults(func=cmd_proj)

    # ----- remove -----
    remove_parser = proj_subparsers.add_parser(
        "rm", help="Remove a project"
    )
    remove_parser.add_argument(
        "title", required=True, help="Project title"
    )
    remove_parser.set_defaults(func=cmd_proj)

    # ----- whoami -----
    whoami_parser = proj_subparsers.add_parser(
        "whoami", help="Show the current project"
    )
    whoami_parser.set_defaults(func=cmd_proj)
