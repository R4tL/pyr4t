"""Utility module for handling file paths related to pyr4t listd."""

import json
from pathlib import Path
from typing import Generic

from .models import EntryType, JSOND4ta

PATH_JSON_PROFILES = Path.home() / ".pyr4t" / "listd.json"
PATH_JSON_PROJECTS = Path.home() / ".pyr4t" / "projects.json"


class _JSONDBM4nager(Generic[EntryType]):
    """
    Manages a JSON DB: add, list, update, select, and remove data
    stored in a JSON file.
    """

    data: JSOND4ta

    def __init__(self, json_file_path: Path):
        self.json_file_path = json_file_path
        self.json_file_path.parent.mkdir(parents=True, exist_ok=True)
        self.json_file_path.touch(exist_ok=True)
        self.data, self.listd, self.current = self._load_data()

    def get_current(self) -> tuple[str, EntryType]:
        """
        Returns the key and entry information ofthe current entry.
        Returns:
            tuple[str, EntryType]: key and entry data of the default entry.
        """

        if not self.current:
            raise ValueError("[error] No current set. Please add entry first.")
        entry = self.listd.get(self.current)
        return self.current, entry

    def update_data(self, key: str, action: str, entry: EntryType = None):
        """
        # TODO: add description
        Args:
            key:
            action:
            entry:
        """


        if not key in self.listd:
            raise ValueError(f"[error] No entry found with key: {key}")
        if action == "add":
            duplicate_key = self._find_duplicate(entry)
            if duplicate_key:
                raise ValueError(
                    f"[error] Entry: {entry}"
                    f"already exists with key '{duplicate_key}'."
                )
        if action in ["updt", "add"] and entry:
            self.listd[key] = entry
            self.data["list"] = self.listd
        elif action == "rm":
            if key == self.current:
                raise ValueError(f"[error] Can't delete current: {key}")
            self.listd.pop(key)
            self.data["list"] = self.listd
        elif action == "slct":
            self.current = key
            self.data["current"] = self.current
        else:
            return
        with open(self.json_file_path, "r+", encoding="utf-8") as file:
            file.seek(0)
            json.dump(self.data, file, indent=4)
            file.truncate()

    def _load_data(self) -> tuple[JSOND4ta, dict[str, EntryType], str]:
        with open(self.json_file_path, "r+", encoding="utf-8") as file:
            try:
                data: dict = json.load(file)
                listd: dict[str, EntryType] = data.get("list", {})
                current: str = data.get("current", "")
            except json.JSONDecodeError:
                listd: dict[str, EntryType] = {}
                current = ""
        return data, listd, current

    def _find_duplicate(self, entry: EntryType) -> str:
        for key, value in self.listd.items():
            if value == entry:
                return key
        return ""