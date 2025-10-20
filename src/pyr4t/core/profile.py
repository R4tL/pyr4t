"""
Profile management for pyr4t.
Handles creation, listing, updating, selection, and removal of user profiles.
"""

import json
from typing import TypedDict

from pyr4t.utils import PATH_JSON_PROFILES


class Profile(TypedDict):
    """Represents a user profile with name and email."""

    name: str
    email: str


Profiles = dict[str, Profile]


class ProfileManager:
    """Manages user profiles: add, list, update, select, and remove profiles stored in a JSON file."""

    def __init__(self):
        PATH_JSON_PROFILES.parent.mkdir(parents=True, exist_ok=True)
        PATH_JSON_PROFILES.touch(exist_ok=True)

    def add_profile(self, alias: str, name: str, email: str):
        """
        Adds a new user profile.
        Args:
            alias (str): Unique identifier for the profile.
            name (str): Name of the user.
            email (str): Email address of the user.
        Raises:
            ValueError: If alias is 'me', already exists, or if a duplicate profile is found.
        """

        if alias == "me":
            raise ValueError("[error] Alias 'me' is reserved for the default profile.")
        with open(PATH_JSON_PROFILES, "r+") as file:
            try:
                data = json.load(file)
                profiles: Profiles = data
            except json.JSONDecodeError:
                profiles = {}

            if alias in profiles:
                raise ValueError(
                    f"[error] Profile with alias '{alias}' already exists."
                )

            duplicate_alias = self._find_duplicate_profiles(name, email)
            if duplicate_alias:
                raise ValueError(
                    f"[error] A profile with name '{name}' and email '{email}' already exists with alias '{duplicate_alias}'."
                )

            profiles[alias] = {"name": name, "email": email}
            if profiles.get("me") is None:
                print(
                    "[info] Setting the first added profile as the default profile 'me'."
                )
                profiles["me"] = {"name": name, "email": email}

            file.seek(0)
            json.dump(profiles, file, indent=4)
            file.truncate()

    def list_profiles(self) -> Profiles:
        """
        Lists all user profiles except the default profile 'me'.
        Returns:
            Profiles: Dictionary of profile aliases to Profile objects.
        """

        with open(PATH_JSON_PROFILES, "r") as file:
            try:
                data = json.load(file)
                profiles: Profiles = data
                profiles.pop("me", None)  # remove default profile from the list
            except json.JSONDecodeError:
                profiles: Profiles = {}
        return profiles

    def remove_profile(self, alias: str):
        """
        Removes a user profile by alias.
        Args:
            alias (str): The alias of the profile to remove.
        Raises:
            ValueError: If attempting to remove the default profile 'me', or if the profile does not exist.
        """

        if alias == "me":
            raise ValueError("[error] Cannot delete the default profile 'me'.")
        with open(PATH_JSON_PROFILES, "r+") as file:
            try:
                profiles: dict[str, dict[str, str]] = json.load(file)
            except json.JSONDecodeError:
                profiles = {}

            if alias not in profiles:
                raise ValueError(f"[error] No profile found with alias '{alias}'.")

            if profiles["me"] == profiles[alias]:
                raise ValueError(
                    "[error] Cannot delete the profile currently set as default 'me'. Please select another profile as default before deleting this one."
                )
            del profiles[alias]

            file.seek(0)
            json.dump(profiles, file, indent=4)
            file.truncate()

    def update_profile(self, alias: str, name: str = None, email: str = None):
        """
        Updates an existing user profile.
        Args:
            alias (str): The alias of the profile to update.
            name (str, optional): New name for the profile.
            email (str, optional): New email for the profile.
        Raises:
            ValueError: If attempting to update the default profile 'me', or if the profile does not exist.
        """

        if alias == "me":
            raise ValueError("[error] Cannot update the default profile 'me'.")
        with open(PATH_JSON_PROFILES, "r+") as file:
            try:
                profiles: dict[str, dict[str, str]] = json.load(file)
            except json.JSONDecodeError:
                profiles = {}

            if alias not in profiles:
                raise ValueError(f"[error] No profile found with alias '{alias}'.")

            if name:
                profiles[alias]["name"] = name
            if email:
                profiles[alias]["email"] = email

            file.seek(0)
            json.dump(profiles, file, indent=4)
            file.truncate()

    def select_profile(self, alias: str):
        """
        Selects a profile as the default profile ('me').
        Args:
            alias (str): The alias of the profile to set as default.
        Raises:
            ValueError: If alias is 'me' or if the profile does not exist.
        """

        if alias == "me":
            raise ValueError("[error] Alias 'me' is reserved for the default profile.")
        with open(PATH_JSON_PROFILES, "r+") as file:
            try:
                profiles: dict[str, dict[str, str]] = json.load(file)
            except json.JSONDecodeError:
                profiles = {}

            if alias not in profiles:
                raise ValueError(f"[error] No profile found with alias '{alias}'.")

            profiles["me"] = profiles[alias]

            file.seek(0)
            json.dump(profiles, file, indent=4)
            file.truncate()

    def whoami(self) -> tuple[str, Profile]:
        """
        Returns the alias and profile information of the current default profile ('me').
        Returns:
            tuple[str, Profile]: Alias and profile data of the default profile.
        """

        with open(PATH_JSON_PROFILES, "r") as file:
            try:
                data = json.load(file)
                profiles: Profiles = data
            except json.JSONDecodeError:
                profiles = {}
        me = profiles.get("me", None)

        if not me:
            raise ValueError(
                "[error] No default profile set. Please add and select a profile first."
            )
        for alias in profiles:
            if profiles[alias] == me:
                return alias, me
        print(
            "[warning] Default profile 'me' does not match any existing profile alias."
        )
        return "me", me

    def _find_duplicate_profiles(self, name: str, emal: str) -> str:
        """Find duplicate profiles by name and email."""
        with open(PATH_JSON_PROFILES, "r") as file:
            try:
                data = json.load(file)
                profiles: Profiles = data
            except json.JSONDecodeError:
                profiles: Profiles = {}

        current = {"name": name, "email": emal}
        for alias, profile in profiles.items():
            if profile == current:
                return alias
        return ""