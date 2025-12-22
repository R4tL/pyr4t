"""Typing."""

from typing import Generic, TypedDict, TypeVar

EntryType = TypeVar("EntryType", bound=TypedDict)


class JSOND4ta(TypedDict):
    """# TODO: add description"""

    current: str
    list: dict[str, EntryType]


class User(TypedDict):
    """# TODO: add description"""

    name: str
    email: str


class Project(TypedDict):
    """# TODO: add description"""

    path: str
    version: str
