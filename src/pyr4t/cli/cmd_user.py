"""
Profile command-line interface for managing Pyr4t profiles.
Provides commands to list, add, select, remove, update,
and show the current profile.
"""

import argparse

from pyr4t.core import ProfileDBM4nager


def cmd_profile(args):
    """
    Handle profile-related CLI actions.
    Args:
        args: Parsed command-line arguments.
    """

    dbmgr = ProfileDBM4nager()

    match args.action:

        case "add":
            dbmgr.add(args.alias, name=args.name, email=args.email)
            print(
                f"[info] Profile added: {args.alias}: {args.name}"
                f" <{args.email}>"
            )

        case "list":
            profiles = dbmgr.list()
            if not profiles:
                print("[warning] No profiles found.")
            else:
                for alias, profile in profiles.items():
                    print(
                        f"[info] {alias}: {profile.get("name", "")} "
                        f"<{profile.get("email", "")}>"
                    )

        case "modify":
            if not args.name and not args.email:
                raise ValueError("Need --name or --email for 'update'")
            dbmgr.modify(args.alias, name=args.name, email=args.email)
            print(f"Profile updated: {args.alias}")

        case "rm":
            dbmgr.remove(args.alias)
            print(f"[info] Profile removed: {args.alias}")

        case "swicth":
            dbmgr.switch(args.alias)
            print(f"[info] Default profile selected: {args.alias}")

        case "whoami":
            alias, profile = dbmgr.whoami()
            print(
                f"[info] {alias}: {profile.get("name", "")} "
                f"<{profile.get("email", "")}>"
            )

def add_profile_parser(subparsers: argparse._SubParsersAction):
    """
    Add the 'profile' command and its subcommands to the CLI parser.
    Args:
        subparsers: The argparse subparsers object to add commands to.
    """

    # Main "profile" parser
    parser: argparse.ArgumentParser = subparsers.add_parser(
        "profile", help="Manage Pyr4t profiles"
    )
    user_subparsers = parser.add_subparsers(dest="action", required=True)

    # ----- add -----
    add_parser = user_subparsers.add_parser("add", help="Add a new profile")
    add_parser.add_argument("alias", required=True, help="Profile alias")
    add_parser.add_argument("name", required=True, help="Profile name")
    add_parser.add_argument("email", required=True, help="Profile email")
    add_parser.set_defaults(func=cmd_profile)

    # ----- list -----
    list_parser = user_subparsers.add_parser("list", help="List profiles")
    list_parser.set_defaults(func=cmd_profile)

    # ----- modify -----
    modify_parser = user_subparsers.add_parser(
        "modify", help="Modify a profile"
    )
    modify_parser.add_argument("alias", required=True, help="Profile alias")
    modify_parser.add_argument("-n", "--name", help="New profile name")
    modify_parser.add_argument("-e", "--email", help="New profile email")
    modify_parser.set_defaults(func=cmd_profile)

    # ----- switch -----
    select_parser = user_subparsers.add_parser(
        "switch", help="Switch current profile"
    )
    select_parser.add_argument("alias", required=True, help="Profile alias")
    select_parser.set_defaults(func=cmd_profile)

    # ----- remove -----
    remove_parser = user_subparsers.add_parser("rm", help="Remove a profile")
    remove_parser.add_argument("alias", required=True, help="Profile alias")
    remove_parser.set_defaults(func=cmd_profile)

    # ----- whoami -----
    whoami_parser = user_subparsers.add_parser(
        "whoami", help="Show the current profile"
    )
    whoami_parser.set_defaults(func=cmd_profile)
