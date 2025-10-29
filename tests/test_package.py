"""Testing package CLI"""

import subprocess
import sys
from pathlib import Path

from .utils import run_cli, make_tmp_venv


def test_package_install(tmp_path: Path):
    """
# TODO: update docstring
    Args:
        tmp_path:
    """

    """Test package install."""

    tmp_venv = make_tmp_venv(tmp_path)
    run_cli("package", "install", "example_pkg",
                  tmp_home=tmp_path, tmp_venv=tmp_venv)



def test_package_uninstall(tmp_path: Path):
    """
# TODO: update docstring
    Args:
        tmp_path:
    """

    """Test package install."""
    subprocess.run()
    tmp_venv = make_tmp_venv(tmp_path)
    out = run_cli("package", "uninstall", "example_pkg",
                  tmp_home=tmp_path, tmp_venv=tmp_venv)
    assert "uninstall" in out.lower() or "removed" in out.lower()