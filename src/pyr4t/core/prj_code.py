"""Module for managing pyr4t project code."""

import ast
import platform
import shutil
import subprocess
import sys
from pathlib import Path

from .prj_db import ProjectDBM4nager


class ProjectCodeM4nager:
    """
    A utility class for managing code for pyr4t projects.
    Args:
        proj_title (str, optional): Title of the project to manage.
            If None, uses the current default project.
    """

    def __init__(self, proj_title: str = None):

        self.dbp = ProjectDBM4nager()
        if proj_title is None:
            proj_title = self.dbp.current
        if proj_title not in self.dbp.listd:
            raise ValueError(f"Project '{proj_title}' not found in DB.")
        self.proj_title = proj_title
        self.proj_path = Path(self.dbp.listd[proj_title]["path"])

    def build(self):
        """Build a binary package of the project."""

        print("[info] Buil binary files ...")
        subprocess.check_call(
            [sys.executable, "-m", "build"], cwd=str(self.proj_path)
        )

    def deploy(self, dev_mode: bool = False):
        """Deploy the package using pip."""

        if dev_mode:
            print("[info] Deploy package in editable mode ...")
            subprocess.check_call(
                [sys.executable, "-m", "pip", "install", "-e", ".[dev]"],
                cwd=str(self.proj_path),
            )
        else:
            print("[info] Deploy permanant package ...")
            subprocess.check_call(
                [sys.executable, "-m", "pip", "install", "."],
                cwd=str(self.proj_path),
            )

    def test(self, specific: str = ""):
        """
        Run tests in `tests` dir.
        Args:
            specific (str): specific test to run (dir, file, file::fuction)
        """

        print(f"[info] Run {Path(self.proj_path).name} tests ...")
        subprocess.check_call(
            [sys.executable, "-m", "pytest", specific],
            cwd=str(self.proj_path / "tests"),
        )

    def run(self, script: str = "main", dev_mode: bool = False):
        """
        Run a script in the `script` dir.
        Args:
            script (str): name of the script
        """

        if dev_mode:
            print(f"[info] Run dev script: {script} ...")
            subprocess.check_call(
                [sys.executable, "-m", script],
                cwd=str(self.proj_path / "dev" / "scripts"),
            )
        else:
            print(f"[info] Run script: {script} ...")
            subprocess.check_call(
                [sys.executable, "-m", script],
                cwd=str(self.proj_path / "scripts"),
            )

    def cls(self, files: list[str] = None):
        """
        Clean cache, logs, or all temporary files.
        Args:
            mode (str): Files to clean.
        """

        if files is None or all(v is None for v in files):
            files = ["cache", "log", "tmp"]

        print(f"[info] Cleaning files {", ".join(v for v in files)} ...")

        if "cache" in files:
            # Remove __pycache__ folders
            cache_count = 0
            for path in self.proj_path.rglob("__pycache__"):
                shutil.rmtree(path, ignore_errors=True)
                cache_count += 1
            print(f"[info] Removed {cache_count} __pycache__ folders.")

            # Remove .pyc and .pyo files
            file_count = 0
            for ext in ("*.pyc", "*.pyo"):
                for file in self.proj_path.rglob(ext):
                    file.unlink(missing_ok=True)
                    file_count += 1
            print(
                f"[info] Deleted {file_count} compiled Python "
                "files (*.pyc, *.pyo)."
            )

        if "log" in files:
            log_count = 0
            for file in self.proj_path.rglob("*.log"):
                file.unlink(missing_ok=True)
                log_count += 1
            print(f"[info] Deleted {log_count} log files.")

        if "tmp" in files:
            for path in self.proj_path.rglob("*"):
                if path.is_dir() and path.name.lower() == "tmp":
                    file_count = 0
                    dir_count = 0
                    for item in path.iterdir():
                        try:
                            if item.is_dir():
                                shutil.rmtree(item, ignore_errors=True)
                                dir_count += 1
                            else:
                                item.unlink(missing_ok=True)
                        except (PermissionError, OSError) as e:
                            print(f"[warning] Could not remove '{item}': {e}")
                            continue
                    print(
                        f"[info] Cleaned tmp '{path}': removed {file_count} "
                        f"files and {dir_count} directories."
                    )

        print("[info] Cleaning complete!")

    def dstr(self, specific: str = ""):
        """
        Manage doscstrings in a folder or file.
        Args:
            specific: specific script in
        """

        # pylint: disable=C0103
        BECON = "# TOD" + "O:"  # Dont interpret as T0D0
        SINGLE_LINE_DOC = f"{BECON} add description"
        GOOGLE_DOC_TEMPLATE = """
{prefix}{args}{returns}
"""
        DO_RETURN_TYPE = f"    {BECON} add return type"
        DO_UPDATE = f"    {BECON} update docstring"

        def generate_google_docstring(
            node: ast.FunctionDef, indent: str, update=False
        ) -> str:
            """
            Generate a Google-style docstring with proper indentation.
            Args:
                node: node
                indent: indentation
                update: if needs update
            Returns:
                str: new docstring
            """

            prefix = f"{DO_UPDATE}" if update else f"{SINGLE_LINE_DOC}"
            fbd_args = ["self", "cls"]
            filtered_args = [
                arg.arg for arg in node.args.args if arg.arg not in fbd_args
            ]
            if (
                node.returns is None
                and not has_non_none_return(node)
                and not filtered_args
            ):
                return f'{indent}"""{prefix}"""\n'
            inner_indent = indent + "    "
            args_lines = "\n".join(
                f"{inner_indent}{arg}:" for arg in filtered_args
            )
            args_section = f"\nArgs:\n{args_lines}" if filtered_args else ""
            if node.returns is not None:
                return_section = (
                    f"\nReturns:\n{inner_indent}{ast.unparse(node.returns)}"
                )
            elif has_non_none_return(node):
                return_section = f"\nReturns:\n{inner_indent}{DO_RETURN_TYPE}"
            else:
                return_section = ""
            docstring_body = GOOGLE_DOC_TEMPLATE.format(
                prefix=prefix, args=args_section, returns=return_section
            )
            for line in docstring_body.splitlines():
                if line.strip() == "":
                    continue
                if not line.startswith(inner_indent) and line not in (
                    DO_RETURN_TYPE,
                    DO_UPDATE,
                ):
                    docstring_body = docstring_body.replace(
                        line, indent + line
                    )
            return f'{indent}"""{docstring_body}{indent}"""\n'

        def check_docstring_needs_update(
            node: ast.FunctionDef, docstring: str
        ) -> bool:
            """
            Check if the docstring is missing any arguments or the return value.
            Args:
                node: node
                docstring: actual doctring
            Returns:
                bool: if needs update
            """

            if docstring is None:
                return True
            filtered_args = [
                arg.arg
                for arg in node.args.args
                if arg.arg not in ("self", "cls")
            ]
            if (
                node.returns is None
                and not has_non_none_return(node)
                and not filtered_args
            ):
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
            """
            Return the whitespace at the start of a line for indentation.
            Args:
                line: line to get indent
            Returns:
                str: indentation
            """

            base = ""
            if ":" in line:
                base = "    "
            return line[: len(line) - len(line.lstrip())] + base

        def process_file(path: Path):
            """
            Manage docstrings in a file.
            Args:
                path: file path.
            """

            with open(path, "r", encoding="utf-8") as f:
                lines = f.read().splitlines()
            if not lines:
                return
            code = "\n".join(lines)
            tree = ast.parse(code)
            edits = []
            if ast.get_docstring(tree) is None:
                edits.append((0, f'"""{SINGLE_LINE_DOC}"""\n'))
            for node in ast.walk(tree):
                if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    if node.name.startswith("_"):
                        continue
                    docstring = ast.get_docstring(node)
                    line_idx = find_signature_end(lines, node.lineno - 1)
                    indent = get_indent(lines[line_idx])
                    if check_docstring_needs_update(node, docstring):
                        edits.append(
                            (
                                line_idx + 1,
                                generate_google_docstring(
                                    node, indent, update=bool(docstring)
                                ),
                            )
                        )
                elif isinstance(node, ast.ClassDef):
                    docstring = ast.get_docstring(node)
                    line_idx = find_signature_end(lines, node.lineno - 1)
                    indent = get_indent(lines[line_idx])
                    if docstring is None:
                        doc = f'{indent}"""{SINGLE_LINE_DOC}"""\n'
                        edits.append((line_idx + 1, doc))
            for lineno, doc in sorted(edits, reverse=True):
                lines.insert(lineno, doc)
            with open(path, "w", encoding="utf-8") as f:
                f.write("\n".join(lines))

        def find_signature_end(lines: list[str], start_line: int) -> int:
            """
            Return the index where the function signature ends.
            Args:
                lines: lines
                start_line: start line
            Returns:
                int: last line
            """

            open_parens = 0
            for i, line in enumerate(lines[start_line:], start=start_line):
                open_parens += line.count("(")
                open_parens -= line.count(")")
                if open_parens <= 0 and line.strip().endswith(":"):
                    return i
            return start_line

        def has_non_none_return(node: ast.FunctionDef) -> bool:
            """
            Return True if the function has at least one 'return' with a value.
            Args:
                node: node
            Returns:
                bool: if has return
            """

            for n in ast.walk(node):
                if isinstance(n, ast.Return) and n.value is not None:
                    return True
            return False

        specific_path = self.proj_path / "src" / specific
        if not specific_path.exists():
            raise FileNotFoundError(f"Path not found: {specific_path}")
        if specific_path.is_file():
            process_file(specific_path)
        if specific_path.is_dir():
            for py_file in specific_path.rglob("*.py"):
                if "Lib" not in str(py_file) and "site-packages" not in str(
                    py_file
                ):
                    print(f"[info] Processing {py_file}")
                    process_file(py_file)

    def fmt(self, specific: str = ""):
        """
        Format code using Black and isort.
        Args:
            specific (str): specific file to format (dir, file, file::fuction)
        """

        specific_path = self.proj_path / "src" / specific
        if not specific_path.exists():
            raise FileNotFoundError(f"Path not found: {specific_path}")
        print("[info] Formatting code...")
        subprocess.check_call(
            [
                sys.executable,
                "-m",
                "black",
                "--line-length",
                "79",
                str(specific_path),
            ]
        )
        subprocess.check_call(
            [sys.executable, "-m", "isort", str(specific_path)]
        )

    def venv(self):
        """Generate a python venv in ./.venv."""

        print("[info] Generating a python venv ...")
        subprocess.check_call(
            [sys.executable, "-m", "venv", str(self.proj_path / ".venv")]
        )
        if platform.system().lower() == "windows":
            activate = str(self.proj_path / ".venv" / "Scripts" / "activate")
        else:
            activate = "source" + str(
                self.proj_path / ".venv" / "bin" / "activate"
            )
        print(f"[info] Activate venv with: {activate}")
