"""Testing users CLI."""

from pathlib import Path

from .utils import run_cli, check_in_file

def test_proj_manage(tmp_path: Path):
    """
    Test proj add.
    """

    path_db_file = tmp_path / ".pyr4t" / "users.json"
    expected_snippet = (
    '"TST1": {\n'
    '            "name": "tester1",\n'
    '            "email": "tester1@mail.com"\n'
    '        },'
    )
    run_cli(
        "user", "add", "TST1", "tester1", "tester1@mail.com",
        tmp_home=tmp_path
    )
    run_cli(
        "user", "add", "TST2", "tester2", "tester2@mail.com",
        tmp_home=tmp_path
    )
    assert check_in_file(path_db_file, expected_snippet, True)
    out_list = run_cli("user", "list", tmp_home=tmp_path)
    assert "TST1" in out_list and "TST2" in out_list
    run_cli(
        "user", "switch", "TST2", tmp_home=tmp_path
    )
    assert check_in_file(path_db_file, '"current": "TST2"', True)
    out_who = run_cli("user", "whoami", tmp_home=tmp_path)
    assert "TST2" in out_who
    run_cli("user", "rm", "TST1", tmp_home=tmp_path)
    assert check_in_file(path_db_file, "TST1", False)
