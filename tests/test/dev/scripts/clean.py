"""
Clean module.
Provides a function to clean cache, logs, and temporary files.
"""

import shutil
from pathlib import Path


def main(mode="all"):
    """Clean cache, logs, or all temporary files."""

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
