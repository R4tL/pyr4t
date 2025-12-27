"""Module for managing a python project architecture."""

import sys
import time
from pathlib import Path

from .prj_db import ProjectDBM4nager
from .usr_db import UserDBM4nager


class ProjectArchM4nager:
    """
    A utility class for managing architecrure for pyr4t projects.
    Args:
        proj_title (str, optional): Title of the project to manage.
            If None, uses the current default project.
        proj_base_path (str, optional): Base path where the project
            is located. If None, uses the path from the projects database.
        authors (list[str], optional): List of authors names.
            If None, uses "current" user.
        proj_version (str, optional): Version of the project.
            If None, uses the version from the projects database.
    """

    def __init__(
        self,
        proj_title: str = None,
        proj_base_path: str = None,
        authors: list[str] = None,
        proj_version: str = None,
    ):

        self.pdb = ProjectDBM4nager()

        if proj_title is None:
            self.proj_title = self.pdb.current
        else:
            self.proj_title = proj_title
        if proj_base_path is None:
            self.proj_path = Path(self.pdb.listd.get(
                self.proj_title, {"": ""}
                ).get("path", ""))
            self.proj_base_path = Path(self.proj_path).parent
        else:
            self.proj_base_path = Path(proj_base_path)
            self.proj_path = self.proj_base_path / self.proj_title
        if proj_version is None:
            self.proj_version = self.pdb.listd.get(
                self.proj_title, {"": ""}
                ).get("version", "")
        else:
            self.proj_version = proj_version
        if authors is None:
            self.authors = ["current"]
        else:
            self.authors = authors

        self._pg = _ProjectGenerator(
            self.proj_title, self.proj_base_path,
            self.authors, self.proj_version
        )


    def generate_app_project(self):
        """Generate a python app architecture."""

        self._pg.generate_project("app")


    def generate_cli_project(self):
        """Generate a python CLI architecture."""

        self._pg.generate_project("cli")


    def generate_lib_project(self):
        """Generate a python lib architecture."""

        self._pg.generate_project("lib")


    def genretate_dev_env(self):
        """Generate a dev env in /dev"""

        print("[info] Generating a dev environment...")
        (self._pg.proj_path / "dev").mkdir()
        print("[info] Cretation of dir: dev")
        (self._pg.proj_path / "dev" / "scripts").mkdir()
        print("[info] Cretation of dir: scripts")
        (self._pg.proj_path / "dev" / "tmp").mkdir()
        print("[info] Cretation of dir: tmp")
        self._pg.generate_scripts(proj_path=self.proj_path / "dev")


class _ProjectGenerator:
    """
    Class to generate a standardized Python project structure with
    configuration files, scripts, and metadata.
    """

    def __init__(
        self,
        proj_title: str,
        base_path: Path,
        authors: list[str],
        proj_version: str,
    ):

        self.proj_title = proj_title.replace(" ", "-")
        self.package_name = self.proj_title.lower().replace("-", "_")
        self.base_path = base_path.resolve()
        self.proj_path = (base_path / self.proj_title).resolve()
        self.authors = self._get_authors(authors)
        self.proj_version = proj_version


    def generate_project(self, project_type: str):
        """
        Create the main project directory and subdirectories.
        Args:
            project_type: Type of project (app, cli, lib)
        Returns:
            bool: True if successful, False otherwise.
        """

        print("[info] Generating a project architecture...")

        # Create main project directory
        self.proj_path.mkdir(parents=True, exist_ok=False)
        print(f"[info] Created project directory: {self.proj_path}")

        # Create dirs
        self._generate_dirs(project_type)

        # Create basic files
        self._generate_init_files(project_type)
        self._generate_gitignore()
        self._generate_py_doc_link()
        self._generate_license()
        self._generate_readme(project_type)
        self._generate_pyproject(project_type)
        self.generate_scripts(project_type=project_type)
        self._generate_tests(project_type)
        models = '''"""Typing variables."""\n'''
        self._create_file(
            self.proj_path / "src" / self.package_name / "models.py", models
        )

        # Create project type files
        if project_type == "app":
            self._generate_app()
        elif project_type == "cli":
            self._generate_cli()
        elif project_type == "lib":
            self._generate_lib()

        # Add to DB and current
        pdb = ProjectDBM4nager()
        pdb.add(
            self.proj_title, str(self.proj_path), self.proj_version
        )
        pdb.switch(self.proj_title)

        print("[info] Project architecture created with success.")


    def generate_scripts(self, proj_path: Path = None, project_type: str = ""):
        """
        Generate 'scripts' directory with example scripts.
        Args:
            parent_path:
            project_type:
        """

        if proj_path is None:
            proj_path = self.proj_path

        if project_type in ["app", "cli"]:
            name = "main.py"
            content = f'''\
"""Run main script."""

from {self.package_name}.__main__ import main as run_main

if __name__ == "__main__":
    run_main()
'''
        else:
            name = "example.py"
            content = '''\
"""A script example."""

def main():
    """Example."""

    print("Script example !")

if __name__ == "__main__":
    main()
'''
        self._create_file(
            proj_path / "scripts" / name, content
        )
        self._create_file(proj_path / "scripts" / "__init__.py")


    def _generate_dirs(self, project_type: str):

        # Init subdirectories list
        subdirs: list[str] = ["docs", "scripts", "src", "tests"]
        subdirs_src: list[str] = ["utils"]
        subdirs_core: list[str] = []
        if project_type in ["app", "cli"]:
            for d in ["cli", "clients", "core", "services"]:
                subdirs_src.append(d)
            if project_type == "app":
                for d in ["api", "gui"]:
                    subdirs_src.append(d)

        # Create subdirectories
        for subdir in subdirs:
            (self.proj_path / subdir).mkdir()
            print(f"[info] Cretation of dir: {subdir}")
        (self.proj_path / "src" / self.package_name).mkdir()
        print(f"[info] Cretation of dir: {self.package_name}")
        for subdir_src in subdirs_src:
            (self.proj_path / "src" / self.package_name / subdir_src).mkdir()
            print(f"[info] Cretation of dir: {subdir_src}")
        for subdir_core in subdirs_core:
            (
                self.proj_path
                / "src"
                / self.package_name
                / "core"
                / subdir_core
            ).mkdir()
            print(f"[info] Cretation of dir: {subdir_core}")


    def _generate_init_files(self, project_type: str):

        for proj_dir in (self.proj_path / "src").rglob(
            "*"
        ):
            if proj_dir.is_dir():
                content = ""
                if proj_dir.name == self.package_name:
                    sub_cont1 = "Exports:\n\tExample (class): Description.\n"
                    sub_cont2 = """\
from .example import Example


__all__ = ['Example']
"""
                    content = f'''\
"""This module provides the main interface for {self.package_name}.
{sub_cont1 if project_type == "lib" else ""}Version: {self.proj_version}"""

{sub_cont2 if project_type == "lib" else ""}
__version__ = "{self.proj_version}"
'''

                elif proj_dir.name == "cli":

                    content = '''\
"""CLI package: provides the parser builder and sub-commands."""

from .parser import build_parser


__all__ = ["build_parser"]
'''

                self._create_file(proj_dir / "__init__.py", content)


    def _generate_py_doc_link(self):
        """
        Create a docs/python_doc.md file with a link to the official
        Python docs.
        """

        docs_path = self.proj_path / "docs" / "python_doc.md"
        content = """\
# Python Documentation
Official Python documentation: [https://docs.python.org/3/](https://docs.python.org/3/)

"""
        self._create_file(docs_path, content)


    def _generate_gitignore(self):
        """
        Create a .gitignore file with standard Python, IDE,
        and OS exclusions.
        """

        content = """\
# Python bytecode
__pycache__/
*.py[cod]
*$py.class

# Virtual environments
venv/
.venv/
.env/
.envrc

# Build / distribution
build/
dist/
*.egg-info/
*.egg

# Development
dev

# Logs
*.log

# IDEs
.idea/
.vscode/
.mypy_cache/
.pytest_cache/

# OS files
.DS_Store
Thumbs.db
"""
        self._create_file(self.proj_path / ".gitignore", content)


    def _generate_readme(self, project_type: str):
        """
        Create a README.md file with project information, installation, usage,
        development, and license sections.
        """

        author_names = ", ".join(a.get("name", "") for a in self.authors)
        cli = f"""\
        
### CLI

* **Run the main project script**

- Integrated CLI
```bash
{self.proj_title.lower()}
```
- Python CLI
```bash
python -m {self.package_name}
```

"""
        lib = f"""\

### Import lib

* **Example**

```python
from {self.package_name} import Example

ex = Example()
ex.example()
```

"""
        # pylint: disable=line-too-long
        content = f"""\
# {self.proj_title} v{self.proj_version}

Short description of the project.

---

## Table of Contents

- [About](#about)
- [Python best practices reminder](#python-best-practices-reminder)
- [Installation](#installation)
- [Requirements](#requirements)
- [Usage](#usage)
- [Development](#development)
- [License](#license)

---

## About

* **Version ->** {self.proj_version}
* **{"Authors" if "," in author_names else "Author"} ->** {author_names}
* **License ->** MIT

---

## Python best practices reminder

### Use a python virtual environment

* **Create a virtual environment**

```bash
python -m venv .venv
```
* **Activate the pyenv**

- Linux/macOS
```bash
source .venv/bin/activate
```

- Windows
```bash
.venv\\Scripts\\activate
```

### Use `pipx`to install the package globally

```bash
pip install pipx
```
```bash
pipx ensurepath
```

---

## Installation using pip or pipx

* **Install directly from GitHub**

- HTTPS
```bash
pip install git+https://github.com/{author_names[0]}/{self.proj_title}.git@v{self.proj_version}
```
```bash
pipx install git+https://github.com/{author_names[0]}/{self.proj_title}.git@v{self.proj_version}
```

- SSH
```bash
pip install git+ssh://github.com/{author_names[0]}/{self.proj_title}.git@v{self.proj_version}
```
```bash
pipx install git+ssh://github.com/{author_names[0]}/{self.proj_title}.git@v{self.proj_version}
```

* **Install directly from Pypi**

```bash
pip install {self.proj_title.lower()}=={self.proj_version}
```
```bash
pipx install {self.proj_title.lower()}=={self.proj_version}
```

* **Cloning the repository**

- Classic mode
```bash
pip install .
```
```bash
pipx install .
```

- Editable mode
```bash
pip install -e .
```

- Developpement mode
```bash
pip install -e .[dev]
```

---

## Requirements

---

## Usage

Go to the root project folder and use the following commands:

### Tests

* **Run the test scripts**
```bash
pytest
```
{cli if project_type in {"cli", "app"} else lib}

---

### Scripts

Go to the root project folder and use the following commands:

* **Run example scripts**
```bash
python -m scripts.manage example
```

---

## License

MIT License. See [LICENSE](LICENSE) for details.
"""
        # pylint: enable=line-too-long
        self._create_file(self.proj_path / "README.md", content)


    def _generate_license(self):
        """
        Create a LICENSE file with the MIT license
        and author information.
        """

        author_names = ", ".join(a.get("name", "") for a in self.authors)
        content = f"""\
MIT License

Copyright (c) {time.strftime("%Y")} {author_names}

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
        self._create_file(self.proj_path / "LICENSE", content)


    def _generate_pyproject(self, project_type: str):
        """
        Create a pyproject.toml file with project metadata,
        dependencies, and build configuration.
        """

        authors_toml = ", ".join(
            [
                f'{{ name = "{a.get("name")}", email = "{a.get("email")}" }}'
                for a in self.authors
            ]
        )
        scripts = f"""\
[project.scripts]
{self.proj_title.lower()} = "{self.package_name}.luncher:core_main"
"""

        content = f"""\
[project]
name = "{self.proj_title}"
version = "{self.proj_version}"
description = ""
authors = [{authors_toml}]
requires-python = ">={f"{sys.version_info.major}.{sys.version_info.minor}"}"
readme = "README.md"
license = {{ file = "LICENSE" }}
dependencies = []

[project.optional-dependencies]
dev = {self._get_dev_dependencies()}
{scripts if project_type in ["cli", "app"] else ""}
[build-system]
requires = ["setuptools>=61.0"]
build-backend = "setuptools.build_meta"

[tool.setuptools.packages.find]
where = ["src"]
"""
        self._create_file(self.proj_path / "pyproject.toml", content)


    def _generate_tests(self, project_type: str):

        test = '''\
"""Test package example."""

import pytest
'''
        if project_type == "lib":
            test += f'''\
            
from {self.package_name}.example import Example


def test_example(capsys):
    """Test that calling Example.example() prints 'Hello World'."""

    ex = Example()
    ex.example()
    captured = capsys.readouterr()
    assert captured.out.strip() == "Hello World"

'''
        elif project_type in ["app", "cli"]:
            test += f'''\
import subprocess
import sys


def test_cli_{self.package_name}(monkeypatch, capsys):
    """Test that running the CLI command prints 'Hello World'."""

    result = subprocess.run(
        [sys.executable, "-m", "{self.package_name}"],
        capture_output=True,
        text=True
    )
    assert result.stdout.strip() == "Hello World !"

    result2 = subprocess.run(
        ["{self.proj_title.lower()}"],
        capture_output=True,
        text=True
    )
    assert result2.stdout.strip() == "Hello World"

'''

        self._create_file(self.proj_path / "tests" / "test_example.py", test)


    def _generate_cli(self):

        # Scripts in CLI dir
        example = '''\
"""CLI command for printing package version."""

import argparse


def cmd_example(args: argparse.Namespace):
    """Print the current version of the package."""

    if args.action == "print":
        a = args.string
        if args.upper:
            a.upper()
        print(a)

def add_example_parser(subparsers: argparse._SubParsersAction):
    """
    Add the --version command to the CLI parser.
    Args:
        subparsers: The subparsers object from the main parser.
    """

    parser: argparse.ArgumentParser = subparsers.add_parser(
    "example", help="Example print cmd"
    )
    example_subparsers = parser.add_subparsers(dest="action", required=True)

    print_parser = example_subparsers.add_parser(
        "print", help="Print user inut"
    )
    print_parser.add_argument("string", help="string to print")
    print_parser.add_argument(
    "-u", "--upper", help="print in capital letters",
    action = "store_true"
    )
    print_parser.set_defaults(func=cmd_example)
'''
        tree = '''\
"""Functions to print a cmd tree."""

import shutil
import json

from pathlib import Path


def wrap_sequence(
    prefix: str,
    connector: str,
    key: str,
    seq_list: list[str],
    have_children: bool,
    desc="",
):
    """Builds wrapped text lines for a tree node with optional
    sequence and description.
    Args:
        prefix (str): The prefix for the current tree level 
        (indentation + connectors).
        connector (str): The connector symbol linking the node to
        its parent (e.g., "├──" or "└──").
        key (str): The name of the current node.
        seq_list (list[str]): A list of elements to display on the
        same line as the key.
        have_children (bool): Whether the node has child elements.
        desc (str, optional): Description text to display on the
        right side of the node.
    Returns:
        list[str]: A list of formatted strings representing this
        node and its wrapped lines.
    """

    # Init term dimentions
    term_width = shutil.get_terminal_size().columns
    desc_width = 2 * term_width // 5
    max_width = term_width - desc_width

    # Init variable for code
    desc_split = wrap_desc(desc, desc_width)
    base_line = f"{prefix}{connector} {key}"
    wrap_connector = "│   " if connector == "├──" else "    "
    if have_children:
        wrap_connector += "│"
    indent = " " * (len(base_line) + 1 - len(prefix + wrap_connector))
    lines = []
    current_line = base_line

    # Check if we can append each elt on one line
    for elem in seq_list:
        elem_str = f" {elem}"
        if len(current_line) + len(elem_str) > max_width - 1:
            # Create a line with this content and we will create a new
            if desc_split:  # add desc
                spaces = " " * (max_width - len(current_line))
                current_line += f"{spaces}{desc_split.pop(0)}"
            lines.append(current_line)
            current_line = (
                prefix + wrap_connector + indent + elem.strip()
            )  # create new line
        else:
            # Can spread on one line
            current_line += elem_str

    # Last line
    if desc_split:
        spaces = " " * (max_width - len(current_line))
        current_line += f"{spaces}{desc_split.pop(0)}"
    lines.append(current_line)
    for line_desc in desc_split:
        spaces = " " * ((max_width) - len(prefix + wrap_connector))
        lines.append(prefix + wrap_connector + spaces + line_desc)

    return lines

def wrap_desc(desc: str, desc_width: int) -> list[str]:
    """
    Wraps a description string to fit within a given width.
    Args:
        desc: The description text to wrap.
        desc_width: The maximum width for each wrapped line.
    Returns:
        list[str]: A list of formatted strings representing
        this node and its wrapped lines.
    """

    words = desc.split(" ")
    lines = []
    current_line = ""
    for word in words:
        # +1 for the space between words if it's not the first word in the line
        extra_len = len(word) + (1 if current_line else 0)
        if len(current_line) + extra_len > desc_width:
            # Line is full -> append it to lines
            lines.append(current_line)
            # For subsequent lines, add indentation
            current_line = "  " + word
        else:
            # Add the word to the current line
            if current_line:
                current_line += " " + word
            else:
                current_line = word
    if current_line:
        lines.append(current_line)
    return lines

def build_lines(dict_cmd: dict, prefix="") -> list[str]:
    """
    Build wraped lines to print dinamicaly.
    Args:
        dict_cmd: dict of commands.
        prefix:
    Returns:
        list[str]: A list of formatted strings.
    """

    lines = []
    items = list(dict_cmd.items())
    for i, (key, value) in enumerate(items):
        connector = "└──" if i == len(items) - 1 else "├──"
        seq_list = value.get("__seq__", [])
        desc = value.get("__desc__", "")
        children = {
            k: v
            for k, v in value.items()
            if isinstance(v, dict) and k not in ("__seq__", "__desc__")
        }
        if desc:
            desc = "# " + desc
        wrapped_lines = wrap_sequence(
            prefix, connector, key, seq_list, children != {}, desc
        )
        lines.extend(wrapped_lines)
        if children:
            extension = "    " if i == len(items) - 1 else "│   "
            lines.extend(build_lines(children, prefix + extension))
    return lines


def get_tree():
    """
    Prints a formatted tree representation commands using commands.json.
    Returns:
        str: The string to print in the terminal.
    """

    with open(
        Path(__file__).parent / "commands.json", encoding="UTF-8"
    ) as file:
        data_cmd = json.load(file)
    lines = build_lines(data_cmd)
    return "\\n".join(lines)
'''
        parser = f'''\
"""
Parser module for the CLI.
Creates the main argument parser and registers subcommands.
"""

import argparse
import sys

from {self.package_name} import __version__
from .command_tree import get_tree
from .cmd_example import add_example_parser


def cmd_base(args: argparse.Namespace):
    """
    Base commands in the root of CLI.
    Args:
        args (argparse.pathspace): Parsed command-line arguments containing
        project details.
    """
    
    if args.help_requested:
        print(get_tree())
        print("")
        build_parser().print_help()
    elif args.version:
        print(f"{self.proj_title} {{__version__}}")
    elif args.command is None:
        print("[error] No command was entered. Use `-h` or `--help` for help.")
    sys.exit(0)

def build_parser() -> argparse.ArgumentParser:
    """Creates and configures the main argument parser for the CLI.
    Returns:
        argparse.ArgumentParser: The configured argument parser for the CLI.
    """
    
    parser = argparse.ArgumentParser(
        prog="{self.proj_title.lower()}",
        description="CLI of {self.proj_title}.",
        add_help=False
    )
    parser.add_argument(
    "-V", "--version", action = "store_true", help="Show version and exit"
    )
    parser.add_argument(
        "-h", "--help", action="store_true",
        dest="help_requested", help="Show help"
    )
    parser.set_defaults(func=cmd_base)
    subparsers = parser.add_subparsers(dest="command")
    subparsers = parser.add_subparsers(dest="command")

    add_example_parser(subparsers)

    return parser
'''
        commands = f"""\
{{
    "{self.proj_title.lower()}": {{
        "__desc__": "{self.proj_title} CLI",
        "__seq__":["[(--help | -h) | (--version | -V)]"],
        "example": {{
        "__desc__": "Example of command",
        "__seq__": ["<script>", "[(--uper | -u)]"]
        }}
    }}
}}
"""

        # Scripts requiered
        main = f'''\
"""
Main module for the project.
Provides the entry point for command-line interface operation.
"""

from .cli import build_parser

def main():
    """Main entry point for the {self.proj_title} CLI program."""
    parser = build_parser()
    args = parser.parse_args()

    if hasattr(args, "func"):
        args.func(args)
    else:
        print("Hello World")  # default comportement

if __name__ == "__main__":
    main()
'''
        luncher = f'''\
"""
Launcher module for the CLI.
Provides the entry point for running the application from the command line.
"""

from {self.package_name}.__main__ import main as core_main


def main():
    """Runs the {self.package_name} application from the command line."""

    core_main()
'''

        self._create_file(
            self.proj_path
            / "src"
            / self.package_name
            / "cli"
            / "cmd_example.py",
            example,
        )
        self._create_file(
            self.proj_path
            / "src"
            / self.package_name
            / "cli"
            / "command_tree.py",
            tree,
        )
        self._create_file(
            self.proj_path / "src" / self.package_name / "cli" / "parser.py",
            parser,
        )
        self._create_file(
            self.proj_path
            / "src"
            / self.package_name
            / "cli"
            / "commands.json",
            commands,
        )

        self._create_file(
            self.proj_path / "src" / self.package_name / "__main__.py", main
        )
        self._create_file(
            self.proj_path / "src" / self.package_name / "luncher.py",
            luncher,
        )


    def _generate_app(self):

        # Need same script like CLI (APP is CLI ++)
        self._generate_cli()

        # GUI
        main_window = '''"""Main window of the app."""\n'''
        dialogs = '''"""Dialog boxes, popups"""\n'''
        styles = '''"""Styles of the app (CSS, theme, colors)."""\n'''
        widgets = '''"""Custom widgets."""\n'''

        # API
        app = '''"""API entry point (FastAPI, Flask)"""\n'''
        routes = '''"""Endpoint definitions."""\n'''
        dependencies = '''"""Dependencies, service injections."""'''
        schemas = '''"""Data schemas (Pydantic)."""\n'''

        self._create_file(
            self.proj_path
            / "src"
            / self.package_name
            / "gui"
            / "main_window.py",
            main_window,
        )
        self._create_file(
            self.proj_path / "src" / self.package_name / "gui" / "dialogs.py",
            dialogs,
        )
        self._create_file(
            self.proj_path / "src" / self.package_name / "gui" / "styles.py",
            styles,
        )
        self._create_file(
            self.proj_path / "src" / self.package_name / "gui" / "widgets.py",
            widgets,
        )

        self._create_file(
            self.proj_path / "src" / self.package_name / "api" / "app.py",
            app,
        )
        self._create_file(
            self.proj_path / "src" / self.package_name / "api" / "routes.py",
            routes,
        )
        self._create_file(
            self.proj_path
            / "src"
            / self.package_name
            / "api"
            / "dependencies.py",
            dependencies,
        )
        self._create_file(
            self.proj_path / "src" / self.package_name / "api" / "schemas.py",
            schemas,
        )


    def _generate_lib(self):

        example = '''\
"""Example of a module for a lib."""

class Example:
    """Example class."""

    def example(self):
        """Example of a function."""

        print("Hello World")
'''
        self._create_file(
            self.proj_path / "src" / self.package_name / "example.py",
            example,
        )


    def _create_file(self, file_path: Path, content: str = ""):
        try:
            file_path.parent.mkdir(parents=True, exist_ok=True)
            with open(file_path, "w", encoding="utf-8") as file:
                file.write(content)
            print(f"[info] Created file: {file_path}")
        except OSError as e:
            print(f"[error] An error occurred while creating {file_path}: {e}")


    def _get_dev_dependencies(self):
        major, minor = sys.version_info[:2]

        # Define recommended versions per Python release
        if major == 3 and minor >= 12:
            pytest = "pytest>=8.3.2"
            black = "black>=24.3.0"
            isort = "isort>=5.13.2"
        elif major == 3 and minor >= 11:
            pytest = "pytest>=8.2.0"
            black = "black>=23.9.0"
            isort = "isort>=5.12.0"
        elif major == 3 and minor >= 10:
            pytest = "pytest>=8.0.0"
            black = "black>=23.3.0"
            isort = "isort>=5.11.0"
        else:
            pytest = "pytest>=7.0.0"
            black = "black>=22.0.0"
            isort = "isort>=5.10.0"

        # Return TOML-style list
        return f'["{pytest}", "{black}", "{isort}"]'


    def _get_authors(self, authors: list[str]) -> list[dict]:
        udb = UserDBM4nager()
        authors_list = []
        for author in authors:
            if author == "current":
                profile = udb.listd.get(udb.current, {})
            else:
                profile = udb.listd.get(author, {})
            if profile:
                authors_list.append(profile)
            else:
                print(
                    f"[warning] No user found for alias '{author}'."
                    " Add new user data:"
                )
                if author == "current":
                    author = input("Alias: ").upper()
                udb.add(
                    author,
                    input(f"`{author}` name: "),
                    input(f"`{author}` email: "),
                )
                authors_list.append({"name": author, "email": ""})
        return authors_list
