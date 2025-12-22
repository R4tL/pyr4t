"""CLI command for managing Pyr4t users."""

import argparse

from pyr4t.core import UserDBM4nager


def cmd_usr(args: argparse.Namespace):
    """
    Handle user-related CLI actions.
    Args:
        args (argparse.pathspace): Parsed command-line arguments containing
        project details.
    """

    dbu = UserDBM4nager()

    match args.action:

        case "add":
            dbu.add(args.alias, name=args.name, email=args.email)

        case "ls":
            users = dbu.list()
            if not users:
                print("[warning] No users found.")
            else:
                for alias, user in users.items():
                    if alias == dbu.current:
                        print(
                            f"* {alias}: {user.get("name", "")} "
                            f"<{user.get("email", "")}>"
                        )
                    else:
                        print(
                            f"  {alias}: {user.get("name", "")} "
                            f"<{user.get("email", "")}>"
                        )

        case "mv":
            if not args.name and not args.email:
                raise ValueError(
                    "Either --name or --email must be specified."
                )
            dbu.modify(args.alias, name=args.name, email=args.email)

        case "rm":
            dbu.remove(args.alias)

        case "switch":
            dbu.switch(args.alias)


def add_usr_parser(subparsers: argparse._SubParsersAction):
    """
    Add the 'user' command and its subcommands to the CLI parser.
    Args:
        subparsers: The argparse subparsers object to add commands to.
    """

    # Main "usr" parser
    parser: argparse.ArgumentParser = subparsers.add_parser(
        "usr", help="Manage Pyr4t users"
    )
    user_subparsers = parser.add_subparsers(dest="action", required=True)

    # ----- add -----
    add_parser = user_subparsers.add_parser("add", help="Add a new user")
    add_parser.add_argument("alias",  help="User alias")
    add_parser.add_argument("name",  help="User name")
    add_parser.add_argument("email",  help="User email")
    add_parser.set_defaults(func=cmd_usr)

    # ----- ls -----
    list_parser = user_subparsers.add_parser("ls", help="List users")
    list_parser.set_defaults(func=cmd_usr)

    # ----- mv -----
    modify_parser = user_subparsers.add_parser("mv", help="Modify a user")
    modify_parser.add_argument("alias",  help="User alias")
    modify_parser.add_argument("-n", "--name", help="New user name")
    modify_parser.add_argument("-e", "--email", help="New user email")
    modify_parser.set_defaults(func=cmd_usr)

    # ----- switch -----
    select_parser = user_subparsers.add_parser(
        "switch", help="Switch current user"
    )
    select_parser.add_argument("alias",  help="User alias")
    select_parser.set_defaults(func=cmd_usr)

    # ----- rm -----
    remove_parser = user_subparsers.add_parser("rm", help="Remove an user")
    remove_parser.add_argument("alias",  help="User alias")
    remove_parser.set_defaults(func=cmd_usr)
