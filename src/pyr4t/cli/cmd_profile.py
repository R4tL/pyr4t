"""
Profile command-line interface for managing Pyr4t profiles.
Provides commands to list, add, select, remove, update, and show the current profile.
"""

import argparse

from pyr4t.core import ProfileManager


def cmd_profile(args):
    """
    Handle profile-related CLI actions.
    Args:
        args: Parsed command-line arguments.
    """

    mgr = ProfileManager()

    if args.action == "list":
        profiles = mgr.list_profiles()
        if not profiles:
            print("[warning] No profiles found.")
        else:
            for alias, profile in profiles.items():
                print(
                    f"[info] {alias}: {profile.get("name", "")} <{profile.get("email", "")}>"
                )

    elif args.action == "add":
        mgr.add_profile(args.alias, name=args.name, email=args.email)
        print(f"[info] Profile added: {args.alias}: {args.name} <{args.email}>")

    elif args.action == "select":
        mgr.select_profile(args.alias)
        print(f"[info] Default profile selected: {args.alias}")

    elif args.action == "remove":
        mgr.remove_profile(args.alias)
        print(f"[info] Profile removed: {args.alias}")

    elif args.action == "update":
        if not args.name and not args.email:
            raise ValueError(
                "For 'update', at least --name or --email must be provided"
            )
        mgr.update_profile(args.alias, name=args.name, email=args.email)
        print(f"Profile updated: {args.alias}")

    elif args.action == "whoami":
        alias, profile = mgr.whoami()
        print(
            f"[info] Current profile: {alias}: {profile.get("name", "")} <{profile.get("email", "")}>"
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
    profile_subparsers = parser.add_subparsers(dest="action", required=True)

    # ----- list -----
    list_parser = profile_subparsers.add_parser("list", help="List profiles")
    list_parser.set_defaults(func=cmd_profile)

    # ----- add -----
    add_parser = profile_subparsers.add_parser("add", help="Add a new profile")
    add_parser.add_argument("-a", "--alias", required=True, help="Profile alias")
    add_parser.add_argument("-n", "--name", required=True, help="Profile name")
    add_parser.add_argument("-e", "--email", required=True, help="Profile email")
    add_parser.set_defaults(func=cmd_profile)

    # ----- select -----
    select_parser = profile_subparsers.add_parser("select", help="Select a profile")
    select_parser.add_argument("-a", "--alias", required=True, help="Profile alias")
    select_parser.set_defaults(func=cmd_profile)

    # ----- remove -----
    remove_parser = profile_subparsers.add_parser("remove", help="Remove a profile")
    remove_parser.add_argument("-a", "--alias", required=True, help="Profile alias")
    remove_parser.set_defaults(func=cmd_profile)

    # ----- update -----
    update_parser = profile_subparsers.add_parser("update", help="Update a profile")
    update_parser.add_argument(
        "-a", "--alias", required=True, help="Alias of the profile to update"
    )
    update_parser.add_argument("-n", "--name", help="New profile name")
    update_parser.add_argument("-e", "--email", help="New profile email")
    update_parser.set_defaults(func=cmd_profile)

    # ----- whoami -----
    whoami_parser = profile_subparsers.add_parser(
        "whoami", help="Show the current profile"
    )
    whoami_parser.set_defaults(func=cmd_profile)