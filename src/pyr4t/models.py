"""Typing module."""

from typing import Generic, TypedDict, TypeVar

EntryType = TypeVar("EntryType", bound=TypedDict)


class JSOND4ta(TypedDict):
    """Typing for JSON data."""

    current: str
    list: dict[str, EntryType]


class User(TypedDict):
    """Typing for user data."""

    name: str
    email: str


class Project(TypedDict):
    """Typing for project data."""

    path: str
    version: str
