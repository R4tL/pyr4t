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
        proj_title (str, optional): title of the project to manage
            (None -> uses the current default project)
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
        """
        Deploy the package using pip.
            Args:
                dev_mode (bool, optional): if True, deploy in editable mode.
        """

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

    def run(self, script: str = "main", dev_mode: bool = False):
        """
        Run a script in the `script` dir.
        Args:
            script (str, optional): name of the script
            dev_mode (bool, optional): if true run dev script
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
            files (list[str], optional): files to clean
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
            specific (str, optional): specific script to process
                (dir, file, file::fuction)
        """

        # pylint: disable=C0103
        BECON = "# TOD" + "O:"  # Dont interpret as T0D0
        FIRST_LINE_DOC = f"{BECON} update docstring"
        GOOGLE_DOC_TEMPLATE = """
{prefix}{args}{returns}
"""
        DO_RETURN_TYPE = f"{BECON} add return type to the fct (-> type)"

        def generate_google_docstring(
            node: ast.FunctionDef, indent: str
        ) -> str:
            """
            Generate a Google-style docstring with proper indentation.
            Args:
                node (ast.FunctionDef): the function node
                indent (str): indentation
            Returns:
                str: new docstring
            """

            prefix = f"{FIRST_LINE_DOC}"
            filtered_args = filter_args(node)

            if (
                node.returns is None
                and not has_non_none_return(node)
                and not filtered_args
            ):
                return f'{indent}"""{prefix}"""'
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
                ):
                    docstring_body = docstring_body.replace(
                        line, indent + line
                    )
            return f'{indent}"""{docstring_body}{indent}"""'

        def check_docstring_needs_update(
            node: ast.FunctionDef, docstring: str
        ) -> bool:
            """
            Check if the docstring is missing any arguments or
            the return value.
            Args:
                node (ast.FunctionDef): the function node
                docstring (str): actual doctring
            Returns:
                bool: if needs update
            """

            if docstring is None:
                return True
            filtered_args = filter_args(node)
            if (
                node.returns is None
                and not has_non_none_return(node)
                and not filtered_args
                ):
                return False
            for arg in filtered_args:
                if arg not in docstring:
                    return True

            if has_non_none_return(node):
                if "Returns" not in docstring:
                    return True
                if node.returns is None and DO_RETURN_TYPE not in docstring:
                    return True
                if (
                    node.returns is not None
                    and (ast.unparse(node.returns)
                    not in docstring.split("Returns:")[1])
                ):
                    return True
            return False

        def get_indent(line: str) -> str:
            """
            Return the whitespace at the start of a line for indentation.
            Args:
                line (str): line to get indent
            Returns:
                str: indentation
            """

            base = ""
            if ":" in line:
                base = "    "
            return line[: len(line) - len(line.lstrip())] + base

        def find_docstring_bounds(
                lines: list[str], start: int
        ) -> tuple[int, int] | None:
            """
            Find the start and end lines of a docstring.
            Args:
                lines (list[str]): lines
                start (int): line to start searching from
            Returns:
                tuple[int, int] | None: start and end lines or None
            """

            if start >= len(lines):
                return None
            if '"""' not in lines[start]:
                return None

            end = start + 1
            while end < len(lines) and '"""' not in lines[end]:
                end += 1

            return start, end + 1

        def process_file(path: Path):
            """
            Manage docstrings in a file.
            Args:
                path (Path): file path
            """

            with open(path, "r", encoding="utf-8") as f:
                lines = f.read().splitlines()
            if not lines:
                return
            code = "\n".join(lines)
            tree = ast.parse(code)
            edits = []
            if ast.get_docstring(tree) is None:
                edits.append((0, f'"""{FIRST_LINE_DOC}"""'))
            for node in ast.walk(tree):
                if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    if node.name.startswith("_"):
                        continue
                    docstring = ast.get_docstring(node)
                    line_idx = find_signature_end(lines, node.lineno - 1)
                    indent = get_indent(lines[line_idx])
                    if check_docstring_needs_update(node, docstring):
                        new_doc = generate_google_docstring(
                            node, indent
                        )
                        insert_at = line_idx + 1
                        if docstring is not None:
                            bounds = find_docstring_bounds(lines, insert_at)
                            if bounds:
                                start, end = bounds
                                del lines[start:end]
                                insert_at = start

                        edits.append((insert_at, new_doc))

                elif isinstance(node, ast.ClassDef):
                    docstring = ast.get_docstring(node)
                    line_idx = find_signature_end(lines, node.lineno - 1)
                    indent = get_indent(lines[line_idx])
                    if docstring is None:
                        doc = f'{indent}"""{FIRST_LINE_DOC}"""'
                        edits.append((line_idx + 1, doc))
            for lineno, doc in sorted(edits, reverse=True):
                lines.insert(lineno, doc)
            with open(path, "w", encoding="utf-8") as f:
                f.write("\n".join(lines))

        def find_signature_end(lines: list[str], start_line: int) -> int:
            """
            Return the index where the function signature ends.
            Args:
                lines (list[str]): lines
                start_line (int): start line
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
                node (ast.FunctionDef): the function node
            Returns:
                bool: if has return
            """

            for n in ast.walk(node):
                if isinstance(n, ast.Return) and n.value is not None:
                    return True
            return False

        def filter_args(node: ast.FunctionDef) -> list[str]:
            """
            Filter out unwanted arguments.
            Args:
                node (ast.FunctionDef): the function node
            Returns:
                list[str]: filtered arguments
            """

            fbd_args = ["self", "cls"]

            # Map argument names to their default values
            defaults = node.args.defaults
            defaults_map = {}
            for i, default in enumerate(defaults):
                arg_index = len(node.args.args) - len(defaults) + i
                defaults_map[node.args.args[arg_index].arg] = default

            # Build argument list
            filtered_args = []
            for arg in node.args.args:
                if arg.arg in fbd_args:
                    continue
                name = arg.arg
                default = defaults_map.get(name)
                if arg.annotation:
                    ann = ast.unparse(arg.annotation)
                    if default:
                        ann = f"{ann}, optional"
                    name = f"{name} ({ann})"
                else:
                    if default:
                        ann = ", optional"
                    else:
                        ann = ""
                    name = f"{name} ({BECON} Add type in fct{ann})"
                filtered_args.append(name)
            return filtered_args

        specific_path = self.proj_path / "src" / specific
        if not specific_path.exists():
            raise FileNotFoundError(f"Path not found: {specific_path}")
        if specific_path.is_file():
            print(f"[info] Processing {specific_path.name}")
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
