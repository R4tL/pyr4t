"""CLI command for managing Pyr4t users."""

import argparse

from pyr4t.core import UserDBM4nager


def cmd_user(args: argparse.Namespace):
    """
    Handle user-related CLI actions.
    Args:
        args: Parsed command-line arguments.
    """

    dbu = UserDBM4nager()

    match args.action:

        case "add":
            dbu.add(args.alias, name=args.name, email=args.email)
            print(
                f"[info] User added: {args.alias}: {args.name}"
                f" <{args.email}>"
            )

        case "list":
            users = dbu.list()
            if not users:
                print("[warning] No users found.")
            else:
                for alias, user in users.items():
                    print(
                        f"[info] {alias}: {user.get("name", "")} "
                        f"<{user.get("email", "")}>"
                    )

        case "modify":
            dbu.modify(args.alias, name=args.name, email=args.email)
            if args.name or args.email:
                print(f"User updated: {args.alias}")

        case "rm":
            dbu.remove(args.alias)
            print(f"[info] User removed: {args.alias}")

        case "swicth":
            dbu.switch(args.alias)
            print(f"[info] Default user selected: {args.alias}")

        case "whoami":
            alias, user = dbu.whoami()
            print(
                f"[info] {alias}: {user.get("name", "")} "
                f"<{user.get("email", "")}>"
            )


def add_user_parser(subparsers: argparse._SubParsersAction):
    """
    Add the 'user' command and its subcommands to the CLI parser.
    Args:
        subparsers: The argparse subparsers object to add commands to.
    """

    # Main "user" parser
    parser: argparse.ArgumentParser = subparsers.add_parser(
        "user", help="Manage Pyr4t users"
    )
    user_subparsers = parser.add_subparsers(dest="action", required=True)

    # ----- add -----
    add_parser = user_subparsers.add_parser("add", help="Add a new user")
    add_parser.add_argument("alias", required=True, help="User alias")
    add_parser.add_argument("name", required=True, help="User name")
    add_parser.add_argument("email", required=True, help="User email")
    add_parser.set_defaults(func=cmd_user)

    # ----- list -----
    list_parser = user_subparsers.add_parser("list", help="List users")
    list_parser.set_defaults(func=cmd_user)

    # ----- modify -----
    modify_parser = user_subparsers.add_parser("modify", help="Modify a user")
    modify_parser.add_argument("alias", required=True, help="User alias")
    modify_parser.add_argument("-n", "--name", help="New user name")
    modify_parser.add_argument("-e", "--email", help="New user email")
    modify_parser.set_defaults(func=cmd_user)

    # ----- switch -----
    select_parser = user_subparsers.add_parser(
        "switch", help="Switch current user"
    )
    select_parser.add_argument("alias", required=True, help="User alias")
    select_parser.set_defaults(func=cmd_user)

    # ----- remove -----
    remove_parser = user_subparsers.add_parser("rm", help="Remove an user")
    remove_parser.add_argument("alias", required=True, help="User alias")
    remove_parser.set_defaults(func=cmd_user)

    # ----- whoami -----
    whoami_parser = user_subparsers.add_parser(
        "whoami", help="Show the current user"
    )
    whoami_parser.set_defaults(func=cmd_user)