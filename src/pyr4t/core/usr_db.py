"""
User management for pyr4t.
Handles creation, listing, updating, selection, and removal of user users.
"""

from pathlib import Path

from pyr4t.models import User
from pyr4t.utils import _JSONDBM4nager


class UserDBM4nager(_JSONDBM4nager[User]):
    """Manages user users: add, list, update, select, and remove users
    stored in a JSON file."""

    def __init__(self):
        super().__init__(Path.home() / ".pyr4t" / "users.json")

    def add(self, alias: str, name: str, email: str):
        """Adds a new user user.

        Args:
            alias (str): unique identifier for the user
            name (str): name of the user
            email (str): email address of the user
        """

        self._validate_email(email)
        user: User = {"name": name, "email": email}
        self.update_data(alias.upper(), "add", user)
        print(f"[info] User added: {alias}: {name} <{email}>")

    def list(self) -> dict[str, User]:
        """Lists all user users except the default user 'me'.

        Returns:
            dict[str, User]: dictionary of user aliases to User objects
        """

        return self.listd

    def remove(self, alias: str):
        """Removes a user user by alias.

        Args:
            alias (str): alias of the user to remove
        """

        self.update_data(alias.upper(), "rm")
        if alias == "*":
            print("[info] All users removed")
        else:
            print(f"[info] User removed: {alias}")

    def modify(self, alias: str, name: str = None, email: str = None):
        """Updates an existing user user.

        Args:
            alias (str): alias of the user to update
            name (str, optional): new name for the user
            email (str, optional): new email for the user
        """

        user = self.listd.get(alias.upper())
        if name:
            user["name"] = name
        if email:
            self._validate_email(email)
            user["email"] = email
        self.update_data(alias.upper(), "updt", user)
        print(
            f"[info] User updated: {alias}: {user.get("name", "")} "
            f"<{user.get("email", "")}>"
        )

    def switch(self, alias: str):
        """Selects a user as the default user.

        Args:
            alias (str): alias of the user to set as default
        """

        self.update_data(alias.upper(), "slct")
        print(f"[info] Default user selected: {alias}")

    def whoami(self) -> tuple[str, User]:
        """Returns the alias and user information of the current user.

        Returns:
            tuple[str, User]: alias and user data of the default user
        """

        return self.get_current()

    def _validate_email(self, email: str):
        """Verifies if the email is valid."""

        if "@" not in email or email.count("@") != 1:
            raise ValueError("Email must contain exactly one '@'")
        local, domain = email.split("@")
        if not local or not domain or "." not in domain:
            raise ValueError("Invalid format for email")
