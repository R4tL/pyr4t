"""Testing prod CLI."""

from pathlib import Path

from .utils import run_cli, make_tmp_venv, ensure_project_init


def test_prod_build(tmp_path: Path):
    """Test prod build."""

    ensure_project_init(tmp_path)
    run_cli("prod", "build", tmp_home=tmp_path)
    assert (tmp_path / "dist").exists()


def test_prod_run(tmp_path: Path):
    """Test prod run."""

    ensure_project_init(tmp_path)
    out = run_cli("prod", "run", "example", tmp_home=tmp_path)
    assert "Script example !" in out

def test_prod_test(tmp_path: Path):
    """Test prod test."""

    ensure_project_init(tmp_path)
    with open(
        tmp_path / "tests" / "test_prod_test.py", "w", encoding="UTF-8"
    ) as f:
        f.write("print('Test OK !')")
    out = run_cli("prod", "test", tmp_home=tmp_path)
    assert "Test OK !" in out


def test_prod_deploy(tmp_path: Path):
    """Test prod deploy."""

    ensure_project_init(tmp_path)
    tmp_venv = make_tmp_venv(tmp_path)
    run_cli("prod", "deploy", tmp_home=tmp_path, tmp_venv=tmp_venv)
    dist_info = list((tmp_path / ".venv").rglob("demo-0.1.0.dist-info"))
    assert dist_info
    assert not (tmp_path / "src" / "demo.egg-info").exists()
