"""
User management for pyr4t.
Handles creation, listing, updating, selection, and removal of user users.
"""

from pyr4t.models import User
from pyr4t.utils import PATH_JSON_PROFILES, _JSONDBM4nager


class UserDBM4nager(_JSONDBM4nager[User]):
    """
    Manages user users: add, list, update, select, and remove users
    stored in a JSON file.
    """

    def __init__(self):
        super().__init__(PATH_JSON_PROFILES)


    def add(self, alias: str, name: str, email: str):
        """
        Adds a new user user.
        Args:
            alias (str): Unique identifier for the user.
            name (str): Name of the user.
            email (str): Email address of the user.
        """

        self._validate_email(email)
        user: User = {"name": name, "email": email}
        self.update_data(alias.upper(), "add", user)
        print(f"[info] User added: {alias}: {name} <{email}>")


    def list(self) -> dict[str, User]:
        """
        Lists all user users except the default user 'me'.
        Returns:
            dict[str, User]: Dictionary of user aliases
            to User objects.
        """

        return self.listd


    def remove(self, alias: str):
        """
        Removes a user user by alias.
        Args:
            alias (str): The alias of the user to remove.
        """

        self.update_data(alias.upper(), "rm")
        print(f"[info] User removed: {alias}")


    def modify(self, alias: str, name: str = None, email: str = None):
        """
        Updates an existing user user.
        Args:
            alias (str): The alias of the user to update.
            name (str, optional): New name for the user.
            email (str, optional): New email for the user.
        """

        user = self.listd.get(alias.upper())
        if name:
            user["name"] = name
        if email:
            self._validate_email(email)
            user["email"] = email
        self.update_data(alias.upper(), "updt", user)
        print(f"[info] User updated: {alias}: {name} <{email}>")


    def switch(self, alias: str):
        """
        Selects a user as the default user ('me').
        Args:
            alias (str): The alias of the user to set as default.
        Raises:
            ValueError: If alias is 'me' or if the user does not exist.
        """

        self.update_data(alias.upper(), "slct")
        print(f"[info] Current user selected: {alias}")


    def whoami(self) -> tuple[str, User]:
        """
        Returns the alias and user information ofthe current user.
        Returns:
            tuple[str, User]: Alias and user data of the default user.
        """

        return self.get_current()


    def _validate_email(self, email: str):
        if "@" not in email or email.count("@") != 1:
            raise ValueError("Email must contain exactly one '@'")
        local, domain = email.split("@")
        if not local or not domain or "." not in domain:
            raise ValueError("Invalid format for email")
