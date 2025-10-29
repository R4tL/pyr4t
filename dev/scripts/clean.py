"""# TODO: add description"""

import shutil
from pathlib import Path


def main(mode="all"):
    """
# TODO: update docstring
    Args:
        mode:
    """

    """Clean cache, logs, or all temporary files."""
    print(f"[info] Cleaning mode: {mode}")

    if mode in ("cache", "all"):
        # Remove __pycache__ folders
        cache_count = 0
        for path in Path(".").rglob("__pycache__"):
            shutil.rmtree(path, ignore_errors=True)
            cache_count += 1
        print(f"[info] Removed {cache_count} __pycache__ folders.")

        # Remove .pyc and .pyo files
        file_count = 0
        for ext in ("*.pyc", "*.pyo"):
            for file in Path(".").rglob(ext):
                file.unlink(missing_ok=True)
                file_count += 1
        print(
            f"[info] Deleted {file_count} compiled Python files (*.pyc, *.pyo)."
        )

    if mode in ("log", "all"):
        log_count = 0
        for file in Path(".").rglob("*.log"):
            file.unlink(missing_ok=True)
            log_count += 1
        print(f"[info] Deleted {log_count} log files.")

    if mode in ("tmp", "all"):
        for path in Path("./dev/tmp").rglob("*"):
            shutil.rmtree(path, ignore_errors=True)

    print("[info] Cleaning complete!")