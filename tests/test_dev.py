"""Testing dev CLI."""

from pathlib import Path

from .utils import run_cli, make_tmp_venv, ensure_project_init


def test_dev_init(tmp_path: Path):
    """Test dev init."""

    ensure_project_init(tmp_path)
    run_cli("dev", "init", tmp_home=tmp_path)
    assert (tmp_path / "dev").exists()


def test_dstr(tmp_path: Path):
    """Test dev dstr."""

    ensure_project_init(tmp_path)
    run_cli("dev", "dstr", tmp_home=tmp_path)
    run_cli("dev", "dstr", "scripts/example")


def test_dev_fmt(tmp_path: Path):
    """Test dev fmt."""

    ensure_project_init(tmp_path)
    run_cli("dev", "fmt", tmp_home=tmp_path)
    run_cli("dev", "fmt", "scripts/example")



def test_dev_cls(tmp_path: Path):
    """Test dev cls."""

    ensure_project_init(tmp_path, dev=True)
    run_cli("dev", "cls", "--cache", tmp_home=tmp_path)
    run_cli("dev", "cls", "--log", tmp_home=tmp_path)
    run_cli("dev", "cls", "--tmp", tmp_home=tmp_path)
    run_cli("dev", "cls", "--tmp", "--cache", tmp_home=tmp_path)
    run_cli("dev", "cls", "--tmp", "--log", tmp_home=tmp_path)
    run_cli("dev", "cls", "--log", "--cache", tmp_home=tmp_path)
    run_cli("dev", "cls", tmp_home=tmp_path)


def test_dev_deploy(tmp_path: Path):
    """Test dev deploy."""

    ensure_project_init(tmp_path)
    tmp_venv = make_tmp_venv(tmp_path)
    run_cli("dev", "deploy", tmp_home=tmp_path, tmp_venv=tmp_venv)
    dist_info = list((tmp_path / ".venv").rglob("demo-0.1.0.dist-info"))
    assert dist_info
    assert (tmp_path / "src" / "demo.egg-info").exists()


def test_dev_venv(tmp_path: Path):
    """Test dev venv."""

    ensure_project_init(tmp_path)
    run_cli("dev", "venv", tmp_home=tmp_path)
    assert (tmp_path / ".venv").exists()
