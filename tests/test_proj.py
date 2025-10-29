"""# TODO: add description"""

from .utils import run_cli
from pathlib import Path


def test_proj_init_with_new_author(tmp_path):
    """
    # TODO: add description
    Args:
        tmp_path:
    """

    inputs = "Alice\nalice@example.com\n"
    out = run_cli(
        "proj", "init", "--cli", "demo", "--authors", "alice",
        tmp_home=tmp_path, inputs=inputs
    )
    assert "added" in out.lower() or "project" in out.lower()


def test_proj_add_and_rm(tmp_path):
    """
    # TODO: add description
    Args:
        tmp_path:
    """

    proj_path = tmp_path / "proj1"
    proj_path.mkdir()
    run_cli("proj", "add", "proj1", str(proj_path), "0.1.0", tmp_home=tmp_path)
    out = run_cli("proj", "rm", "proj1", tmp_home=tmp_path)
    assert "removed" in out.lower()


def test_proj_list(tmp_path):
    """
    # TODO: add description
    Args:
        tmp_path:
    """

    out = run_cli("proj", "list", tmp_home=tmp_path)
    assert "project" in out.lower() or "none" in out.lower()


def test_proj_switch(tmp_path):
    """
    # TODO: add description
    Args:
        tmp_path:
    """

    run_cli("proj", "switch", "proj1", tmp_home=tmp_path, check=False)