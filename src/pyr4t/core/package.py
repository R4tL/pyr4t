"""Fuctions to manage pyr4t packges."""

import platform
import subprocess
import sys
import tempfile
from pathlib import Path

import requests


def install_pyr4tpackage(package: str, version: str = None):
    """
    Install a pyr4t package from a binary (wheel or tar.gz) GitHub release
    without relying on Git.
    Args:
        package (str): package name
        version (str, optional): version to install. If "": latest release.
    """

    # URL GitHub API
    if version:
        url = (
            "https://api.github.com/packages/R4tL/"
            f"{package}/releases/tags/v{version}"
        )
    else:
        url = f"https://api.github.com/packages/R4tL/{package}/releases/latest"

    headers = {}
    response = requests.get(url, timeout=5)

    if response.status_code != 200:
        raise RuntimeError(
            f"[{response.status_code}] GitHub API: {response.text}"
        )

    # Token management
    if response.status_code in (401, 403):  # need token
        need_input_tok = False
        token_file = Path().home() / ".pyr4t" / "token"
        if token_file.exists():
            with open(token_file, "r", encoding="utf-8") as f:
                token = f.read()
            headers["Authorization"] = f"token {token}"
            response = requests.get(url, headers=headers, timeout=5)
            if response.status_code in (401, 403):  # invalid token
                need_input_tok = True
        if need_input_tok:
            token = input("Token: ")
            headers["Authorization"] = f"token {token}"
            response = requests.get(url, headers=headers, timeout=5)
            if response.status_code in (401, 403):  # invalid token
                raise RuntimeError(
                    f"[{response.status_code}] Invalid token: {response.text}"
                )
            with open(token_file, "w", encoding="utf-8") as f:
                f.write(token)
            print(f"[info] Token added in {token_file}")

    release: dict = response.json()
    assets: list[dict] = release.get("assets", [])
    if not assets:
        raise RuntimeError("No binary found in this release.")

    # Determine asset
    py_version = f"cp{sys.version_info.major}{sys.version_info.minor}"
    os_tag = platform.system().lower()  # 'linux', 'darwin', 'windows'

    # First find pure python wheel
    asset = next(
        (a for a in assets if a["name"].endswith("py3-none-any.whl")), None
    )

    # If not, find specific wheel for OS and Python
    if not asset:
        asset = next(
            (
                a
                for a in assets
                if a["name"].endswith(".whl")
                and py_version in a["name"].lower()
                and os_tag in a["name"].lower()
            ),
            None,
        )

    # If not, fallback a tar.gz
    if not asset:
        asset = next(
            (a for a in assets if a["name"].endswith(".tar.gz")), None
        )

    if not asset:
        raise RuntimeError(
            "No compatible file (.whl or .tar.gz) found for"
            " your system and Python."
        )

    download_url = asset["browser_download_url"]
    print(f"[info] Downloading {asset['name']} from {download_url} ...")

    # DL tmp file
    suffix = Path(asset["name"]).suffix
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp_file:
        r = requests.get(download_url, headers=headers, stream=True, timeout=5)
        r.raise_for_status()
        for chunk in r.iter_content(chunk_size=8192):
            tmp_file.write(chunk)
        tmp_path = Path(tmp_file.name)

    # DL with pip
    print("[info] Installing with pip ...")
    subprocess.check_call(
        [sys.executable, "-m", "pip", "install", str(tmp_path)]
    )

    # RM tmp file
    tmp_path.unlink()
    print(f"[info] Installation of {package} finished")


def upgrade_pyr4tpackage(package: str, version):
    """
    Upgrade a pyr4t package.
    Args:
        package (str): package name
        version (str, optional): version to install. If "": latest release.
    """

    install_pyr4tpackage(package, version)


def downgrade_pyr4tpackage(package: str, version: str):
    """
    Downgrade a pyr4t package.
    Args:
        package (str): package name
        version (str): version to install.
    """

    install_pyr4tpackage(package, version)


def uninstall_pyr4tpackage(package: str):
    """
    Uninstall a pyr4t package.
    Args:
        package (str): Name of the package to uninstall.
    """

    print(f"[info] Uninstalling {package} with pip ...")
    subprocess.check_call(
        [sys.executable, "-m", "pip", "uninstall", "-y", package]
    )
    print(f"[info] Uninstallation of {package} finished")
