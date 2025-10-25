import ast
import subprocess
import sys
from pathlib import Path

BECON = "# TOD" + "O:"  # Dont interpret as T0-D0
SINGLE_LINE_DOC = f"{BECON} add description"
GOOGLE_DOC_TEMPLATE = """
{prefix}{args}{returns}
"""
DO_RETURN_TYPE = f"    {BECON} add return type"
DO_UPDATE = f"{BECON} update docstring"


def main():
    """Format code and check docstrings."""
    pack_path = Path(__file__).parents[2] / "src" / "pyr4t"
    format_code(pack_path)
    dctr(pack_path)


def format_code(path: Path):
    """Format code using Black and isort."""
    print("[info] Formatting code...")
    try:
        subprocess.run(
            [sys.executable, "-m", "black", "--line-length", "79", str(path)],
            check=True,
        )
        subprocess.run([sys.executable, "-m", "isort", str(path)], check=True)
        print("[info] Code formatted successfully!")
    except subprocess.CalledProcessError:
        print("[warning] Formatting failed.")


def dctr(folder: Path):
    """Manage doscstrings in a folder."""
    for py_file in folder.rglob("*.py"):
        print(f"[info] Processing {py_file}")
        process_file(py_file)


def generate_google_docstring(
    node: ast.FunctionDef, indent: str, update=False
) -> str:
    """Generate a Google-style docstring with proper indentation."""
    prefix = f"{DO_UPDATE}" if update else f"{SINGLE_LINE_DOC}"
    filtered_args = [
        arg.arg for arg in node.args.args if arg.arg not in ("self", "cls")
    ]
    if (
        node.returns is None
        and not has_non_none_return(node)
        and not filtered_args
    ):
        return f'{indent}"""{prefix}"""\n'
    inner_indent = indent + "    "
    args_lines = "\n".join(f"{inner_indent}{arg}:" for arg in filtered_args)
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
            docstring_body = docstring_body.replace(line, indent + line)
    return f'{indent}"""{docstring_body}{indent}"""\n'


def check_docstring_needs_update(
    node: ast.FunctionDef, docstring: str
) -> bool:
    """Check if the docstring is missing any arguments or the return value."""
    if docstring is None:
        return True
    filtered_args = [
        arg.arg for arg in node.args.args if arg.arg not in ("self", "cls")
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
    """Return the whitespace at the start of a line for indentation."""
    base = ""
    if ":" in line:
        base = "    "
    return line[: len(line) - len(line.lstrip())] + base


def process_file(path: Path):
    """Manage docstrings in a file."""
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
    """Return the index where the function signature ends."""
    open_parens = 0
    for i, line in enumerate(lines[start_line:], start=start_line):
        open_parens += line.count("(")
        open_parens -= line.count(")")
        if open_parens <= 0 and line.strip().endswith(":"):
            return i
    return start_line


def has_non_none_return(node: ast.FunctionDef) -> bool:
    """Return True if the function has at least one 'return' with a value."""
    for n in ast.walk(node):
        if isinstance(n, ast.Return) and n.value is not None:
            return True
    return False
