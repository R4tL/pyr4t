"""# TODO: add description"""

from .utils import run_cli


def test_user_add(tmp_path):
    """
    # TODO: add description
    Args:
        tmp_path:
    """

    out = run_cli("user", "add", "alice", "Alice", "alice@example.com", tmp_home=tmp_path)
    assert "added" in out.lower()


def test_user_list(tmp_path):
    """
    # TODO: add description
    Args:
        tmp_path:
    """

    out = run_cli("user", "list", tmp_home=tmp_path)
    assert "alice" in out or "user" in out.lower()


def test_user_modify(tmp_path):
    """
    # TODO: add description
    Args:
        tmp_path:
    """

    out = run_cli("user", "modify", "alice", "--email", "new@example.com", tmp_home=tmp_path)
    assert "modified" in out.lower() or "updated" in out.lower()


def test_user_switch(tmp_path):
    """
    # TODO: add description
    Args:
        tmp_path:
    """

    out = run_cli("user", "switch", "alice", tmp_home=tmp_path)
    assert "active" in out.lower() or "switched" in out.lower()


def test_user_rm(tmp_path):
    """
    # TODO: add description
    Args:
        tmp_path:
    """

    out = run_cli("user", "rm", "alice", tmp_home=tmp_path)
    assert "removed" in out.lower()