"""
Project generator for Python projects.
This module provides the GenerateProject class, which automates the creation of a standardized Python project structure,
including directories, configuration files, scripts, and metadata. It supports customization of project name, version,
authors, and base path, and generates files such as README, LICENSE, .gitignore, pyproject.toml, and Makefiles.
"""

import json
import sys
import time
from pathlib import Path

from pyr4t.utils import PATH_JSON_PROFILES

# TODO : V 1.0.0 ajouter un argument pour choisir le license (MIT, GPL, Apache, etc.)


class GenerateProject:
    """Class to generate a standardized Python project structure with configuration files, scripts, and metadata."""

    def __init__(
        self,
        project_name: str,
        base_path: str = ".",
        project_version: str = "0.1.0",
        authors: list[str] = ["me"],
    ):
        self.project_name = project_name.replace(" ", "-").lower()
        self.package_name = self.project_name.replace("-", "_")
        self.project_path = Path(base_path) / self.project_name
        self.authors = self._get_authors(authors)
        self.project_version = project_version

    def generate_project(self):
        """Generate the entire Python project structure and configuration files."""

        print(
            f"[info] Generating project '{self.project_name}' at {self.project_path}..."
        )
        if not self.create_project_structure():
            exit(1)
        self.create_gitignore()
        self.create_readme()
        self.create_license()
        self.create_py_doc_link()
        self.create_luncher()
        self.create_pyproject()
        self.create_cli_base()
        self.create_basic_scritps()
        self.create_dev_scritps()
        print("[info] Project generation complete.")

    def create_project_structure(self) -> bool:
        """
        Create the main project directory and subdirectories.
        Returns:
            bool: True if successful, False otherwise.
        """

        print("[info] Creating project structure...")
        try:
            # Create main project directory
            self.project_path.mkdir(parents=True, exist_ok=False)
            print(f"[info] Created project directory: {self.project_path}")

            # Create subdirectories
            subdirs = ["docs", "scripts", "src", "tests", "dev"]
            subdirs_dev = ["tmp", "scripts"]
            subdirs_src = ["core", "api", "cli"]

            for subdir in subdirs:
                if subdir == "src":
                    for sub_subdir_src in subdirs_src:
                        (
                            self.project_path
                            / subdir
                            / self.package_name
                            / sub_subdir_src
                        ).mkdir(parents=True, exist_ok=True)
                        print(
                            f"[info] Created subdirectory: {self.project_path / subdir / self.package_name / sub_subdir_src}"
                        )
                elif subdir == "dev":
                    for sub_subdir_dev in subdirs_dev:
                        (self.project_path / subdir / sub_subdir_dev).mkdir(
                            parents=True, exist_ok=True
                        )
                    print(
                        f"[info] reated subdirectory: {self.project_path / subdir / sub_subdir_dev}"
                    )
                else:
                    (self.project_path / subdir).mkdir(parents=True, exist_ok=True)
                    print(f"[info] Created subdirectory: {self.project_path / subdir}")

            for dir in self.project_path.rglob("*"):
                if dir.is_dir():
                    if dir.name not in [
                        "docs",
                        "src",
                        "tests",
                        self.package_name,
                        "cli",
                        "dev",
                        "tmp"
                    ]:
                        self._create_file(dir / "__init__.py")
                    if dir.name == self.package_name:
                        self._create_file(
                            dir / "__init__.py",
                            f'__version__ = "{self.project_version}"\n',
                        )
                        self._create_file(
                            dir / "__main__.py",
                            "def main():\n    print('Hello, World!')\n\nif __name__ == '__main__':\n    main()\n",
                        )
                        dir / "__init__.py"
                        ut_content = '''"""
Utils module.
A collection of reusable utility functions for general purposes.
"""
'''
                        self._create_file(dir / "utils.py", ut_content)

        except FileExistsError:
            print(f"[error] The directory '{self.project_path}' already exists.")
            return False
        except Exception as e:
            print(f"[error] An error occurred: {e}")
            return False
        return True

    def create_py_doc_link(self):
        """Create a docs/python_doc.md file with a link to the official Python docs."""

        docs_path = self.project_path / "docs" / "python_doc.md"
        CONTENT = """# Python Documentation
Official Python documentation: [https://docs.python.org/3/](https://docs.python.org/3/)
"""
        self._create_file(docs_path, CONTENT)

    def create_gitignore(self):
        """Create a .gitignore file with standard Python, IDE, and OS exclusions."""

        print("[info] Creating .gitignore file...")
        CONTENT = """# Python bytecode
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
dev/tmp/

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
        self._create_file(self.project_path / ".gitignore", CONTENT)

    def create_readme(self):
        """Create a README.md file with project information, installation, usage, development, and license sections."""

        print("[info] Creating README file...")
        author_names = ", ".join(a.get("name", "") for a in self.authors)
        CONTENT = f"""# {self.project_name} v{self.project_version}

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

* **Version ->** {self.project_version}
* **{"Authors" if "," in author_names else "Author"} ->** {author_names}
* **License ->** MIT

---

## Python best practices reminder

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
.venv\Scripts\\activate
```

---

## Installation

* **Install directly from GitHub**

- HTTPS
```bash
pip install git+https://github.com/R4tL/{self.project_name}.git@v{self.project_version}
```

- SSH
```bash
pip install git+ssh://github.com/R4tL/{self.project_name}.git@v{self.project_version}
```

* **Install directly from Pypi**

```bash
pip install {self.project_name}=={self.project_version}
```

* **Cloning the repository**

- Classic mode
```bash
pip install .
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

### Install `make` (*optional*)

If you want to have acces to the `make` commands.

* **Linux/macOS**
```bash
sudo apt install make # (or brew / xbps-install)
```

* **Windows (with Chocolatey)**

```bash
choco install make
```

---

## Usage

### CLI

* **Run the main project script**

- Integrated CLI
```bash
run-{self.project_name}
```
- Python CLI
```bash
python -m {self.package_name}
```

### Make commands

Go to the root project folder and use the following commands:

* **Build the project for prod**
```bash
make build
```

* **Run test scripts**
```bash
make test
```

### Scripts

Go to the root project folder and use the following commands:

* **Run test scripts**
```bash
python -m scripts.manage -t
```

---

## Development

### Tests

* **Run tests**
```bash
pytest
```

### Make commands

Go to the root project folder and use the following commands:

* **Create a py venv in .venv**
```bash
make -C dev venv
```

* **Build the project in dev mode**
```bash
make -C dev build
```

* **Run the main project**

- Without args
```bash
make -C dev run
```
- With args
```bash
make -C dev run ARGS="arg1 arg2"
```

* **Format the codebase and manage docstrings**

```bash
make -C dev fmt
```

* **Clean files**

- All
```bash
make -C dev clean
```
```bash
make -C dev clean all
```
- Cache only
```bash
make -C dev clean cache
```
- Logs only
```bash
make -C dev clean log
```
- Files in /dev/tmp only
```bash
make -C dev clean tmp
```

### Scripts

Go to the root project folder and use the following commands:

* **Run the main project**

- Without args
```bash
python -m dev.scripts.manage -r
```
- With args
```bash
python -m dev.scripts.manage -r arg1 arg2
```

* **Format the codebase and manage docstrings**

```bash
python -m dev.scripts.manage -f
```

* **Clean files**

- All
```bash
python -m dev.scripts.manage -c
```
```bash
python -m dev.scripts.manage -c all
```
- Cache only
```bash
python -m dev.scripts.manage -c cache
```
- Logs only
```bash
python -m dev.scripts.manage -c log
```
- Files in /dev/tmp only
```bash
python -m dev.scripts.manage -c tmp
```

---

## License

MIT License. See [LICENSE](LICENSE) for details.
"""
        self._create_file(self.project_path / "README.md", CONTENT)

    def create_license(self):
        """Create a LICENSE file with the MIT license and author information."""

        print("[info] Creating LICENSE file...")
        author_names = ", ".join(a.get("name", "") for a in self.authors)
        CONTENT = f"""MIT License

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
        self._create_file(self.project_path / "LICENSE", CONTENT)

    def create_pyproject(self):
        """Create a pyproject.toml file with project metadata, dependencies, and build configuration."""

        print("[info] Creating pyproject file...")
        PY_VERSION = f"{sys.version_info.major}.{sys.version_info.minor}"
        dev_deps = self._get_dev_dependencies()
        authors_toml = ", ".join(
            [
                f'{{ name = "{a.get("name","")}", email = "{a.get("email","")}" }}'
                for a in self.authors
            ]
        )

        CONTENT = f"""[project]
name = "{self.project_name}"
version = "{self.project_version}"
description = ""
authors = [{authors_toml}]
requires-python = ">={PY_VERSION}"
readme = "README.md"
license = {{ file = "LISENSE" }}
dependencies = []

[project.optional-dependencies]
dev = {dev_deps}

[project.scripts]
{self.project_name} = "{self.package_name}.luncher:main"

[build-system]
requires = ["setuptools>=61.0"]
build-backend = "setuptools.build_meta"

[tool.setuptools.packages.find]
where = ["src"]
"""
        self._create_file(self.project_path / "pyproject.toml", CONTENT)

    def create_luncher(self):
        """Create a CLI runner script for the project."""

        print("[info] Creating CLI runner script...")
        CONTENT = f'''"""
Launcher module for the CLI.
Provides the entry point for running the application from the command line.
""" 

from {self.package_name}.__main__ import main as core_main


def main():
    """Runs the {self.package_name} application from the command line."""

    core_main()
'''
        self._create_file(
            self.project_path / "src" / self.package_name / "luncher.py",
            CONTENT,
        )

    def create_basic_scritps(self):
        """Create basic utility scripts for testing and project management."""

        print("[info] Creating basic scripts...")

        RUN_TEST = """\"\"\"
Run tests module.
Contains a main function to run all project tests using pytest.
\"\"\"

import subprocess


def main():
    \"\"\"Run all project tests using pytest.\"\"\"

    print("[info] Running tests...")
    try:
        subprocess.run(["pytest", "tests"], check=True)
        print("[info] All tests passed!")
    except subprocess.CalledProcessError:
        print("[warning] Some tests failed.")
"""

        MANAGE = f"""\"\"\"
Management CLI module.
Provides a command-line interface to run tests and other project management tasks.
\"\"\"

import argparse
from . import run_tests


def main():
    \"\"\"Main entry point for the management CLI.\"\"\"

    parser = argparse.ArgumentParser(
        description="Project utility CLI for common development tasks."
    )

    parser.add_argument("-t", "--tests", action="store_true", help="Run tests using pytest")
    args = parser.parse_args()

    if args.tests:
        run_tests.main()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
"""

        MAKEFILE = f"""# -------------------------------------------
# pyr4t Makefile
# -------------------------------------------

# Variables
PYTHON := python
MODE ?= classic    # For build (optional extra arguments)

# -------------------------------------------
# Default target
# -------------------------------------------
help:
\t@echo ""
\t@echo "[help] Available commands:"
\t@echo "  build MODE=prod   - Build project in prod mode with pip"
\t@echo "  test              - Run tests"
\t@echo ""

# -------------------------------------------
# Build project
# -------------------------------------------
build:
\t@echo "[info] Build in production mode..."
\t$(PYTHON) -m pip install .
\t@echo "[info] Build complete."

# -------------------------------------------
# Run test scripts
# -------------------------------------------
test:
\t@echo "[info] Running test scripts..."
\t$(PYTHON) -m scripts.manage -t
\t@echo "[info] Tests complete."
"""
        self._create_file(self.project_path / "scripts" / "run_tests.py", RUN_TEST)
        self._create_file(self.project_path / "scripts" / "manage.py", MANAGE)
        self._create_file(self.project_path / "Makefile", MAKEFILE)
        print("[info] Basic scripts created.")

    def create_dev_scritps(self):
        """Create development utility scripts for formatting, cleaning, and managing the project."""

        print("[info] Creating dev scripts...")

        CLEAN = """\"\"\"
Clean module.
Provides a function to clean cache, logs, and temporary files.
\"\"\"

import shutil
from pathlib import Path


def main(mode="all"):
    \"\"\"Clean cache, logs, or all temporary files.\"\"\"

    print(f"[info] Cleaning mode: {mode}")

    if mode in ("cache", "all"):
        cache_count = 0
        for path in Path(__file__).parents[2].rglob("__pycache__"):
            shutil.rmtree(path, ignore_errors=True)
            cache_count += 1
        print(f"[info] Removed {cache_count} __pycache__ folders.")

        file_count = 0
        for ext in ("*.pyc", "*.pyo"):
            for file in Path(__file__).parents[2].rglob(ext):
                file.unlink(missing_ok=True)
                file_count += 1
        print(f"[info] Deleted {file_count} compiled Python files (*.pyc, *.pyo).")

    if mode in ("log", "all"):
        log_count = 0
        for file in Path(__file__).parents[2].rglob("*.log"):
            file.unlink(missing_ok=True)
            log_count += 1
        print(f"[info] Deleted {log_count} log files.")
    
    if mode in ("tmp", "all"):
        tmp_count = 0
        for path in Path("./dev/tmp").rglob("*"):
            shutil.rmtree(path, ignore_errors=True)
        print(f"[info] Deleted {tmp_count} tmp files.")

    print("[info] Cleaning complete!")
"""

        FORMAT = f"""\"\"\"
Format code module.
Provides functions to format code and manage docstrings.
\"\"\"

import subprocess
import sys
from pathlib import Path
import ast


BECON = "# TOD" + "O:"  # Dont interpret as T0-D0
SINGLE_LINE_DOC = f"{{BECON}} add description"
GOOGLE_DOC_TEMPLATE = f\"\"\"
{{{{prefix}}}}{{{{args}}}}{{{{returns}}}}
\"\"\"
DO_RETURN_TYPE = f"    {{{{BECON}}}} add return type"
DO_UPDATE = f"{{{{BECON}}}} update docstring"

def main():
    \"\"\"Format code and check docstrings.\"\"\"

    pack_path = Path(__file__).parents[2].resolve() / "src" / "{self.package_name}"
    format_code(pack_path)
    process_folder(pack_path)
    
def format_code(path: Path):
    \"\"\"Format code using Black and isort.\"\"\"

    print("[info] Formatting code...")
    try:
        subprocess.run([sys.executable, "-m", "black", str(path)], check=True)
        subprocess.run([sys.executable, "-m", "isort", str(path)], check=True)
        print("[info] Code formatted successfully!")
    except subprocess.CalledProcessError:
        print("[warning] Formatting failed.")

def process_folder(folder: Path):
    \"\"\"Manage docstrings in a folder.\"\"\"

    for py_file in folder.rglob("*.py"):
        print(f"[info] Processing {{py_file}}")
        process_file(py_file)

def generate_google_docstring(node: ast.FunctionDef, indent: str, update=False) -> str:
    \"\"\"Generate a Google-style docstring with proper indentation.\"\"\"

    prefix = f"{{DO_UPDATE}}" if update else f"{{SINGLE_LINE_DOC}}"
    filtered_args = [arg.arg for arg in node.args.args if arg.arg not in ("self", "cls")]
    if node.returns is None and not has_non_none_return(node) and not filtered_args:
        return f'{{indent}}\"\"\"{{prefix}}\"\"\"\\n'
    inner_indent = indent + "    "
    args_lines = "\\n".join(f"{{inner_indent}}{{arg}}:" for arg in filtered_args)
    args_section = f"\\nArgs:\\n{{args_lines}}" if filtered_args else ""
    if node.returns is not None:
        return_section = f"\\nReturns:\\n{{inner_indent}}{{ast.unparse(node.returns)}}"
    elif has_non_none_return(node):
        return_section = f"\\nReturns:\\n{{inner_indent}}{{DO_RETURN_TYPE}}"
    else:
        return_section = ""
    docstring_body = GOOGLE_DOC_TEMPLATE.format(prefix=prefix, args=args_section, returns=return_section)
    for line in docstring_body.splitlines():
        if line.strip() == "":
            continue
        if not line.startswith(inner_indent) and line not in (DO_RETURN_TYPE, DO_UPDATE):
            docstring_body = docstring_body.replace(line, indent + line)
    return f'{{indent}}\"\"\"{{docstring_body}}{{indent}}\"\"\"\\n'

def check_docstring_needs_update(node: ast.FunctionDef, docstring: str) -> bool:
    \"\"\"Check if the docstring is missing any arguments or the return value.\"\"\"

    if docstring is None:
        return True
    filtered_args = [arg.arg for arg in node.args.args if arg.arg not in ("self", "cls")]
    if node.returns is None and not has_non_none_return(node) and not filtered_args:
        return False
    for arg in filtered_args:
        if arg not in docstring:
            return True
    if (
        node.returns is not None
        and has_non_none_return(node)
        and "Returns" not in docstring 
        and ast.unparse(node.returns) not in docstring
        and ast.unparse(node.returns) != "None"
        ):
        return True
    return False

def get_indent(line: str) -> str:
    \"\"\"Return the whitespace at the start of a line for indentation.\"\"\"

    base = ""
    if ":" in line:
        base = "    "
    return line[:len(line) - len(line.lstrip())] + base

def process_file(path: Path):
    \"\"\"Manage docstrings in a file.\"\"\"

    with open(path, "r", encoding="utf-8") as f:
        lines = f.read().splitlines()
    if not lines:
        return
    code = "\\n".join(lines)
    tree = ast.parse(code)
    edits = []
    if ast.get_docstring(tree) is None:
        edits.append((0, f'\"\"\"{{SINGLE_LINE_DOC}}\"\"\"\\n'))
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            if node.name.startswith("_"):
                continue
            docstring = ast.get_docstring(node)
            line_idx = find_signature_end(lines, node.lineno - 1)
            indent = get_indent(lines[line_idx])
            if check_docstring_needs_update(node, docstring):
                edits.append((
                    line_idx + 1, 
                    generate_google_docstring(node, indent, update= bool(docstring))
                ))
        elif isinstance(node, ast.ClassDef):
            docstring = ast.get_docstring(node)
            line_idx = find_signature_end(lines, node.lineno - 1)
            indent = get_indent(lines[line_idx])
            if docstring is None:
                doc = f'{{indent}}\"\"\"{{SINGLE_LINE_DOC}}\"\"\"\\n'
                edits.append((line_idx + 1, doc))
    for lineno, doc in sorted(edits, reverse=True):
        lines.insert(lineno, doc)
    with open(path, "w", encoding="utf-8") as f:
        f.write("\\n".join(lines))

def find_signature_end(lines: list[str], start_line: int) -> int:
    \"\"\"Return the index where the function signature ends.\"\"\"

    open_parens = 0
    for i, line in enumerate(lines[start_line:], start=start_line):
        open_parens += line.count("(")
        open_parens -= line.count(")")
        if open_parens <= 0 and line.strip().endswith(":"):
            return i
    return start_line

def has_non_none_return(node: ast.FunctionDef) -> bool:
    \"\"\"Return True if the function has at least one 'return' with a value.\"\"\"

    for n in ast.walk(node):
        if isinstance(n, ast.Return) and n.value is not None:
            return True
    return False
"""

        MANAGE = f"""\"\"\"
Development management CLI module.
Provides a CLI to format code and clean the project.
\"\"\"

import argparse
from . import format_code, clean


def main():
    \"\"\"Main entry point for the development management CLI.\"\"\"

    parser = argparse.ArgumentParser(
        description="Project utility CLI for common development tasks."
    )

    parser.add_argument("-f", "--format", action="store_true", help="Format code with black and isort")
    parser.add_argument(
        "-c", "--clean",
        nargs="?",
        const="cache",  
        choices=["all", "cache", "log", "tmp"],
        help="Clean files: 'all' (default), 'cache', 'log' (log files), or 'tmp' (files in /dev/tmp/)"
    )

    args = parser.parse_args()

    if args.format:
        format_code.main()
    elif args.clean:
        clean.main(args.clean)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
"""

        MAKEFILE = f"""# -------------------------------------------
# pyr4t Development Makefile
# -------------------------------------------

# Variables
PYTHON := python
TYPE ?= all        # For clean (default: all)
ARGS ?=            # For run (optional extra arguments)

# -------------------------------------------
# Default target
# -------------------------------------------
help:
\t@echo ""
\t@echo "[help] Available commands:"
\t@echo "  build             - Build project in dev mode with pip"
\t@echo "  run ARGS="..."  - Run the main project script with optional args"
\t@echo "  fmt               - Format code using black and isort"
\t@echo "  clean TYPE=all    - Clean files: all, cache, log, tmp"
\t@echo "  venv              - Create python venv on .venv"
\t@echo ""

# -------------------------------------------
# Run main script
# -------------------------------------------
run:
\t@echo "[info] Running main project..."
\t$(PYTHON) -m {self.package_name} $(ARGS)
\t@echo "[info] Run complete."

# -------------------------------------------
# Format code
# -------------------------------------------
fmt:
\t$(PYTHON) -m scripts.manage -f

# -------------------------------------------
# Clean project
# -------------------------------------------
clean:
\t$(PYTHON) -m scripts.manage -c $(TYPE)

# -------------------------------------------
# Create venv
# -------------------------------------------
venv:
ifeq ($(OS),Windows_NT)
\t@if not exist "..\.venv" ( \\
\t\techo [info] Creating virtual environment... && \\
\t\t$(PYTHON) -m venv ..\\.venv && \\
\t\techo [info] Venv creation complete. \\
\t) else ( \\
\t\techo [info] Virtual environment already exists, skipping creation. \\
\t)
\t@echo [info] To activate the venv: .\\.venv\\Scripts\\activate
else
\t@if [ ! -d "../.venv" ]; then \\
\t\techo "[info] Creating virtual environment..."; \\
\t\t$(PYTHON) -m venv ../.venv; \\
\t\techo "[info] Venv creation complete."; \\
\telse \\
\t\techo "[info] Virtual environment already exists, skipping creation."; \\
\tfi
\t@echo "[info] To activate the venv: source ./.venv/bin/activate"
endif

# -------------------------------------------
# Build project in dev mode
# -------------------------------------------
build:
\t@echo "[info] Build in development mode..."
\t$(PYTHON) -m pip install -e ..[dev]
\t@echo "[info] Build complete."
"""

        self._create_file(self.project_path / "dev" / "scripts" / "clean.py", CLEAN)
        self._create_file(
            self.project_path / "dev" / "scripts" / "format_code.py", FORMAT
        )
        self._create_file(self.project_path / "dev" / "scripts" / "manage.py", MANAGE)
        self._create_file(self.project_path / "dev" / "Makefile", MAKEFILE)
        MAKEFILE
        print("[info] Dev scripts created.")

    def create_cli_base(self):
        """Create the logic of the command manager with command `--version`."""

        VERSION = f'''"""
Version command for the CLI.
Provides a parser for the --version option.
""" 

import argparse

from pyr4t import __version__


def cmd_version(args: argparse.Namespace):
    """Print the current version of the package."""

    print(__version__)

def add_version_parser(subparsers: argparse._SubParsersAction):
    """Add the --version command to the CLI parser."""

    parser: argparse.ArgumentParser = subparsers.add_parser(
        "--version", help="Print the version of package {self.package_name}"
    )
    parser.set_defaults(func=cmd_version)
'''

        PARSER = f"""\"\"\"
Parser module for the CLI.
Creates the main argument parser and registers subcommands.
\"\"\"

from .cmd_version import add_version_parser


def build_parser():
    \"\"\"Creates and configures the main argument parser for the CLI.
    Returns:
        argparse.ArgumentParser: The configured argument parser for the CLI.
    \"\"\"
    
    parser = argparse.ArgumentParser(
        prog="{self.project_name}", description="CLI of {self.project_name}."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    add_version_parser(subparsers)

    return parser
"""
        INIT = """\"\"\"CLI package: provides the parser builder and sub-commands.\"\"\"

from .parser import build_parser


__all__ = ["build_parser"]
"""

        self._create_file(
            self.project_path / "src" / self.package_name / "cli" / "cmd_version.py",
            VERSION,
        )
        self._create_file(
            self.project_path / "src" / self.package_name / "cli" / "parser.py", PARSER
        )
        self._create_file(
            self.project_path / "src" / self.package_name / "cli" / "__init__.py", INIT
        )

        MAIN = f"""\"\"\"
Main module for the project.
Provides the entry point for command-line interface operation.
\"\"\"

from pyr4t.cli import build_parser

def main():
    \"\"\"Main entry point for the {self.project_name} CLI program.\"\"\"
    parser = build_parser()
    args = parser.parse_args()

    if hasattr(args, "func"):
        args.func(args)
    else:
        print("Hello World")  # default comportement

if __name__ == "__main__":
    main()
"""

        # If, in the future we want run this separatly
        path_main = self.project_path / "src" / self.package_name / "__main__.py"
        if path_main.exists():
            with open(path_main, "w") as file:
                file.write(MAIN)
        else:
            self._create_file(path_main, MAIN)

    def _create_file(self, file_path: Path, content: str = ""):
        try:
            file_path.parent.mkdir(parents=True, exist_ok=True)
            with open(file_path, "w") as file:
                file.write(content)
            print(f"[info] Created file: {file_path}")
        except Exception as e:
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
        authors_list = []
        for author in authors:
            with open(PATH_JSON_PROFILES, "r") as file:
                try:
                    profiles = json.load(file)
                except json.JSONDecodeError:
                    profiles = {}
                profile = profiles.get(author, {})
                if profile:
                    authors_list.append(profile)
                else:
                    print(
                        f"[warning] No profile found for alias '{author}'. Using alias as name."
                    )
                    authors_list.append({"name": author, "email": ""})
        return authors_list