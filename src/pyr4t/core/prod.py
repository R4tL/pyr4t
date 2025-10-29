"""Functions to manage prod mode."""

import subprocess
import sys

from pathlib import Path
from .project import ProjectDBM4nager


pdb = ProjectDBM4nager()
proj_path = Path(pdb.listd.get(pdb.current, {"": ""}).get("path", ""))

def run(script: str):
    """
    Run a script in the `script` dir.
    Args:
        script (str): name of the script
    """

    print(f"[info] Run {script} ...")
    subprocess.check_call(
        [sys.executable, "-m", script], cwd=str(proj_path / "scripts")
    )

def test(specific: str):
    """
    Run tests in `tests` dir
    Args:
        specific (str): specific test to run (dir, file, file::fuction)
    """

    print(f"[info] Run tests {specific} ...")
    subprocess.check_call(
    [sys.executable, "-m", "pytest", specific],
    cwd=str(proj_path / "tests")
    )

def build():
    """Build a binary package of the project."""

    print("[info] Buil binary files ...")
    subprocess.check_call(
        [sys.executable, "-m", "build"], cwd=str(proj_path)
    )

def deploy():
    """Deploy the package using pip."""

    print("[info] Deploy permanant package ...")
    subprocess.check_call(
        [sys.executable, "-m", "pip", "install", "."], cwd=str(proj_path)
    )