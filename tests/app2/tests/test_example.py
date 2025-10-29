"""Test package example."""

import subprocess
import sys

import pytest


def test_cli_app2(monkeypatch, capsys):
    """
# TODO: update docstring
    Args:
        monkeypatch:
        capsys:
    """

    """Test that running the CLI command prints 'Hello World'."""

    result = subprocess.run(
        [sys.executable, "-m", "app2"], capture_output=True, text=True
    )
    assert result.stdout.strip() == "Hello World !"

    result2 = subprocess.run(["app2"], capture_output=True, text=True)
    assert result2.stdout.strip() == "Hello World"