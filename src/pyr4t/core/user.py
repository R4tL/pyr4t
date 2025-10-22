"""
Profile management for pyr4t.
Handles creation, listing, updating, selection, and removal of user profiles.
"""

from pyr4t.models import Profile
from pyr4t.utils import PATH_JSON_PROFILES, _JSONDBM4nager


class ProfileDBM4nager(_JSONDBM4nager[Profile]):
    """
    Manages user profiles: add, list, update, select, and remove profiles
    stored in a JSON file.
    """

    def __init__(self):
        super().__init__(PATH_JSON_PROFILES)

    def add(self, alias: str, name: str, email: str):
        """
        Adds a new user profile.
        Args:
            alias (str): Unique identifier for the profile.
            name (str): Name of the user.
            email (str): Email address of the user.
        """

        profile: Profile = {"name": name, "email": email}
        self.update_data(alias, "add", profile)

    def list(self) -> dict[str, Profile]:
        """
        Lists all user profiles except the default profile 'me'.
        Returns:
            dict[str, Profile]: Dictionary of profile aliases
            to Profile objects.
        """

        return self.listd

    def remove(self, alias: str):
        """
        Removes a user profile by alias.
        Args:
            alias (str): The alias of the profile to remove.
        """

        self.update_data(alias, "rm")

    def modify(self, alias: str, name: str = None, email: str = None):
        """
        Updates an existing user profile.
        Args:
            alias (str): The alias of the profile to update.
            name (str, optional): New name for the profile.
            email (str, optional): New email for the profile.
        """

        profile = self.listd.get(alias)
        if name:
            profile["name"] = name
        if email:
            profile["email"] = email
        self.update_data(alias, "updt", profile)

    def switch(self, alias: str):
        """
        Selects a profile as the default profile ('me').
        Args:
            alias (str): The alias of the profile to set as default.
        Raises:
            ValueError: If alias is 'me' or if the profile does not exist.
        """

        self.update_data(alias, "slct")

    def whoami(self) -> tuple[str, Profile]:
        """
        Returns the alias and profile information ofthe current profile.
        Returns:
            tuple[str, Profile]: Alias and profile data of the default profile.
        """

        return self.get_current()