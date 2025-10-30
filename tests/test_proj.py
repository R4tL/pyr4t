"""Testing proj CLI."""

import subprocess
import sys

from pathlib import Path

from .utils import run_cli, check_in_file


def test_proj_init_with_new_author(tmp_path: Path):
    """
    Test proj init.
    """

    inputs = "Alice\nalice@example.com\n"
    run_cli(
        "proj", "init", "--app", "demoapp", "--authors", "alice",
        tmp_home=tmp_path, inputs=inputs
    )
    run_cli(
        "proj", "init", "--cli", "democli", "--authors", "alice",
        tmp_home=tmp_path, inputs=inputs
    )
    run_cli(
        "proj", "init", "--lib", "demolib", "--authors", "alice",
        tmp_home=tmp_path, inputs=inputs
    )

    app = subprocess.run(
        [sys.executable, "-m", "demoapp.scripts.main"],
        cwd=tmp_path, capture_output=True, text=True, check=True
    )
    cli = subprocess.run(
        [sys.executable, "-m", "democli.scripts.main"],
        cwd=tmp_path, capture_output=True, text=True, check=True
    )
    lib = subprocess.run(
        [sys.executable, "-m", "demolib.scripts.example"],
        cwd=tmp_path, capture_output=True, text=True, check=True
    )
    app_out = app.stdout
    cli_out = cli.stdout
    lib_out = lib.stdout

    assert "Hello World" in app_out
    assert "Hello World" in cli_out
    assert "Script example !" in lib_out
    assert (tmp_path / "democli").exists()
    assert (tmp_path / "demolib").exists()
    assert (tmp_path / "demoapp").exists()


def test_proj_manage(tmp_path: Path):
    """
    Test proj add.
    """

    path_db_file = tmp_path / ".pyr4t" / "projects.json"
    proj1_path = tmp_path / "proj1"
    proj2_path = tmp_path / "proj2"
    proj1_path.mkdir()
    proj2_path.mkdir()
    expected_snippet = (
    '"proj1": {\n'
    f'            "path": "{proj1_path}",\n'
    '            "versison": "0.1.0"\n'
    '        },'
    )
    run_cli(
        "proj", "add", "proj1", str(proj1_path), "0.1.0", tmp_home=tmp_path
    )
    run_cli(
        "proj", "add", "proj2", str(proj2_path), "0.1.0", tmp_home=tmp_path
    )
    assert check_in_file(path_db_file, expected_snippet, True)
    out_list = run_cli("proj", "list", tmp_home=tmp_path)
    assert "proj1" in out_list and "proj2" in out_list
    run_cli(
        "proj", "switch", "proj2", tmp_home=tmp_path
    )
    assert check_in_file(path_db_file, '"current": "proj2"', True)
    out_who = run_cli("proj", "whoami", tmp_home=tmp_path)
    assert "proj2" in out_who
    run_cli("proj", "rm", "proj1", tmp_home=tmp_path)
    assert check_in_file(path_db_file, "proj1", False)
