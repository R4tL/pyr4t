"""Utility module for handling file paths related to pyr4t listd."""

import json
import os
import platform
import re
import shlex
import subprocess
from pathlib import Path
from typing import Generic

from .exceptions import Pyr4tValueError, Pyr4tRuntimeError, Pyr4tFileError
from .models import EntryTypeT, JSOND4ta


class _JSONDBM4nager(Generic[EntryTypeT]):
    """Manages a JSON DB: add, list, update, select, and remove data
    stored in a JSON file."""

    data: JSOND4ta

    def __init__(self, json_file_path: Path):
        self.json_file_path = json_file_path
        self.json_file_path.parent.mkdir(parents=True, exist_ok=True)
        self.json_file_path.touch(exist_ok=True)
        self.data, self.listd, self.current = self._load_data()

    def get_current(self) -> tuple[str, EntryTypeT]:
        """Returns the key and entry information ofthe current entry.

        Returns:
            tuple[str, EntryTypeT]: key and entry data of the default entry
        
        Raises:
            Pyr4tValueError: If no current entry is set.
        """

        if not self.current:
            raise Pyr4tValueError("No current set. Please add entry first.")
        entry = self.listd.get(self.current)
        return self.current, entry

    def update_data(self, key: str, action: str, entry: EntryTypeT = None):
        """Update DB.

        Args:
            key (str): Data key.
            action (str): type (add, rm, updt)
            entry (EntryTypeT): data
        
        Raises:
            Pyr4tValueError: If the action is invalid.
        """

        if not key:
            raise Pyr4tValueError("Key can't be empty.")

        if action == "add":
            k, v = entry.items()
            if not k or not v:
                raise Pyr4tValueError("Entry can't be empty.")
            duplicate_key = self._find_duplicate(entry)
            if duplicate_key:
                raise Pyr4tValueError(
                    f"Entry: {entry} "
                    f"already exists with key '{duplicate_key}'."
                )
            key = self._increment_key(key)

        elif not key in self.listd:
            if key != "*" and action != "rm":
                raise Pyr4tValueError(f"No entry found with key: {key}")

        if action in ["updt", "add"] and entry:
            try:
                self.listd[key] = entry
            except KeyError as e:
                raise Pyr4tValueError(
                    f"No entry found with key: {key}"
                ) from e
            self.data["list"] = self.listd
            if not self.current:
                print("[info] Adding first entry like current")
                self.current = key
                self.data["current"] = self.current
        elif action == "rm":
            if key == self.current:
                self.current = ""
                self.data["current"] = ""
            if key == "*":
                self.listd = {}
                self.current = ""
                self.data = {}
            else:
                try:
                    self.listd.pop(key)
                    self.data["list"] = self.listd
                except KeyError as e:
                    raise Pyr4tValueError(
                        f"No entry found with key: {key}"
                    ) from e
        elif action == "slct":
            self.current = key
            self.data["current"] = self.current
        else:
            return
        with open(self.json_file_path, "r+", encoding="utf-8") as file:
            file.seek(0)
            json.dump(self.data, file, indent=4)
            file.truncate()

    def _load_data(self) -> tuple[JSOND4ta, dict[str, EntryTypeT], str]:
        """Loads datas in the JSON file."""

        with open(self.json_file_path, "r+", encoding="utf-8") as file:
            try:
                data: dict = json.load(file)
                listd: dict[str, EntryTypeT] = data.get("list", {})
                current: str = data.get("current", "")
            except json.JSONDecodeError:
                data: dict = {}
                listd: dict[str, EntryTypeT] = {}
                current = ""
        return data, listd, current

    def _find_duplicate(self, entry: EntryTypeT) -> str:
        """Finds duplicate datas in the JSON file."""

        for key, value in self.listd.items():
            if value == entry:
                return key
        return ""

    def _increment_key(self, key: str) -> str:
        """Increment key if the input already exists in the JSON file."""

        if key not in self.listd:
            return key
        base_key = key
        suffix = 1
        if "_" in key and key.rsplit("_", 1)[-1].isdigit():
            base_key = key.rsplit("_", 1)[0]
            suffix = int(key.rsplit("_", 1)[-1]) + 1
        new_key = f"{base_key}_{suffix}"
        while new_key in self.listd:
            suffix += 1
            new_key = f"{base_key}_{suffix}"
        print(
            f"[warning] Key already exists: {key}. Incremented to: {new_key}"
        )
        return new_key


def select_python_interpreter(python: str = None) -> str:
    """Select a Python interpreter to use for execution.

    Args:
        python (str, optional): Path to or name of the Python interpreter.
            If None, attempts to use the interpreter from the active virtual
            environment. Defaults to None.

    Returns:
        str: The path to a working Python interpreter.

    Raises:
        Pyr4tRuntimeError: If no python interpreter is specified and no active
            virtual environment is found.
        Pyr4tFileError: If the specified python interpreter path does not
            exist or is not a file.
    """

    if not python:
        venv = os.environ.get("VIRTUAL_ENV", "")
        if venv:
            if platform.system().lower() == "windows":
                python = str(Path(venv) / "Scripts" / "python.exe")
            else:
                python = str(Path(venv) / "bin" / "python")
        else:
            raise Pyr4tRuntimeError(
                "No python interpreter specified and no active venv found."
            )
    if not Path(python).exists():
        py_arg = shlex.split(python)
    elif Path(python).is_file():
        py_arg = [python]
    else:
        raise Pyr4tFileError(f"Python interpreter not found: {python}")
    return _check_python_works(py_arg)


def _check_python_works(python_cmd: list[str]) -> str:
    """Checks if the python bin works."""

    out = subprocess.check_output(
        [*python_cmd, "-c", "import sys; print(sys.executable)"], text=True
    ).strip()
    return out


def is_text_valid(text: str) -> bool:
    """Checks if the input string is valid.

    Args:
        text (str): input string to validate

    Returns:
        bool: True if the input string is valid, False otherwise
    """

    return bool(re.fullmatch(r"[A-Za-z0-9_-]+", text))
