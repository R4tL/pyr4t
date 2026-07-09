"""Typing module."""

from typing import TypedDict, TypeVar

EntryTypeT = TypeVar("EntryTypeT", bound=dict[str, str])


class JSOND4ta(TypedDict):
    """Typing for JSON data."""

    current: str
    list: dict[str, EntryTypeT]


class User(TypedDict):
    """Typing for user data."""

    name: str
    email: str


class Project(TypedDict):
    """Typing for project data."""

    path: str
    version: str
