"""Utils for tests."""

import subprocess
import os
from pathlib import Path
import venv


def make_tmp_venv(tmp_path: Path):
    """
# TODO: update docstring
    Args:
        tmp_path:
    Returns:
            # TODO: add return type
    """

    """Create an isolated virtualenv and return its bin path."""
    env_dir = tmp_path / ".venv"
    venv.EnvBuilder(with_pip=True).create(env_dir)
    bin_path = env_dir / ("Scripts" if os.name == "nt" else "bin")
    return bin_path


def run_cli(
        *args,
        inputs: str = None,
        tmp_home: Path = None,
        tmp_venv: Path = None,
        check: bool = True
    ) -> str:
    """
    Run a Pyr4t CLI command and return stdout/stderr as string.

    Args:
        *args: CLI args (e.g. "proj", "list")
        inputs (str): stdin input for interactive commands
        tmp_home (Path): temporary PYR4T_HOME dir
        tmp_venv (Path): path to a temporary venv's bin folder
        check (bool): assert success (default True)
    Returns:
        str: stdout or stderr of the command
    """
    env = os.environ.copy()

    if tmp_home:
        env["PYR4T_HOME"] = str(tmp_home)

    if tmp_venv:
        # Make sure pip/python commands inside CLI use this isolated venv
        env["PATH"] = f"{tmp_venv}{os.pathsep}{env['PATH']}"
        env["VIRTUAL_ENV"] = str(tmp_venv.parent)

    result = subprocess.run(
        ["pyr4t", *args],
        input=inputs,
        capture_output=True,
        text=True,
        env=env,
        check=False,
    )

    print(f"\n> pyr4t {' '.join(args)}")
    print(result.stdout or result.stderr)

    if check and result.returncode != 0:
        raise AssertionError(
            f"Command failed ({result.returncode}): "
            f"pyr4t {' '.join(args)}\n{result.stderr}"
        )

    return (result.stdout or result.stderr).strip()


def ensure_project_init(
        tmp_home: Path,
        title: str = "demo",
        authors: str = None,
        dev: bool = False
    ):
        """
# TODO: update docstring
        Args:
            tmp_home:
            title:
            authors:
            dev:
        """

    """
    Initialize a minimal Pyr4t project so that dev/prod commands can run.
    """
    if authors is None:
        authors = "alice"

    inputs = "Alice\nalice@example.com\n"
    run_cli(
        "proj", "init", "--lib", title,
        "--authors", authors,
        tmp_home=tmp_home,
        inputs=inputs
    )
    if dev:
        run_cli("dev", "init")