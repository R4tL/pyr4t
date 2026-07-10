"""Functions to manage pyr4t packges."""

import platform
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

import keyring
import requests

from pyr4t.exceptions import Pyr4tRuntimeError
from pyr4t.utils import select_python_interpreter


def install_pyr4tpackage(
    package: str, version: str = None, python: str = None
):
    """Install a pyr4t package from a binary (wheel or tar.gz) GitHub release
    without relying on Git.

    Args:
        package (str): package name
        version (str, optional): version to install (None -> latest release)
        python (str, optional): python interpreter to use

    Raises:
        Pyr4tRuntimeError: If the GitHub API request fails or if the package
            cannot be installed.
    """

    python_cmd = select_python_interpreter(python)
    print(f"[info] Using Python interpreter: {python_cmd}")
    # URL GitHub API
    if version:
        url = (
            "https://api.github.com/repos/R4tL/"
            f"{package}/releases/tags/v{version}"
        )
    else:
        url = f"https://api.github.com/repos/R4tL/{package}/releases/latest"

    headers = {}
    token = load_token()
    if token:
        headers["Authorization"] = f"token {token}"
    r = requests.get(url, headers=headers, timeout=5)

    if r.status_code in (401, 403, 404):  # need token / not found (nf)
        raise Pyr4tRuntimeError(
            f"[{r.status_code}] "
            "Access denied or release not found. "
            "If the package is private, please provide a valid token "
            "using `pyr4t install --token <token>`."
        )
    elif r.status_code != 200:
        raise Pyr4tRuntimeError(
            f"[{r.status_code}] GitHub API error : {r.text}"
        )

    release: dict = r.json()
    assets: list[dict] = release.get("assets", [])
    if not assets:
        raise Pyr4tRuntimeError("No binary found in this release.")

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
        raise Pyr4tRuntimeError(
            "No compatible file (.whl or .tar.gz) found for"
            " your system and Python."
        )

    # download_url = asset["browser_download_url"] # old way
    download_url = asset["url"]
    headers["Accept"] = "application/octet-stream"
    print(f"[info] Downloading {asset['name']} from {download_url} ...")

    # DL tmp file
    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_file = Path(tmp_dir) / str(asset["name"])
        with requests.get(
            download_url, headers=headers, stream=True, timeout=10
        ) as r:
            r.raise_for_status()
            with open(tmp_file, "wb") as f:
                shutil.copyfileobj(r.raw, f)
        # DL with pip
        print("[info] Installing with pip ...")
        subprocess.check_call(
            [python_cmd, "-m", "pip", "install", str(tmp_file)]
        )

    print(f"[info] Installation of {package} finished")


def install_info(show_private: bool = False):
    """Print information about available pyr4t packages.

    Args:
        show_private (bool, optional): show private repositories
    
    Raises:
        Pyr4tRuntimeError: If the GitHub API request fails or if a private
            repository cannot be accessed.
    """

    print(
        "[info] Fetching pyr4t package list from"
        " GitHub (can take a while)..."
    )

    headers = {}
    token = load_token()
    if token and show_private:
        headers["Authorization"] = f"token {token}"
        url = "https://api.github.com/user/repos"
    elif show_private:
        raise Pyr4tRuntimeError(
            "Private token required to show private repos."
        )
    else:
        url = "https://api.github.com/users/R4tL/repos"

    # First attempt (no token)
    r = requests.get(url, headers=headers, timeout=10)

    if r.status_code in (401, 403, 404):  # need token / not found (nf)
        raise Pyr4tRuntimeError(
            f"[{r.status_code}] Invalid token: {r.text}. "
            "Please provide a valid token "
            "using `pyr4t install --token <token>`."
        )
    elif r.status_code != 200:
        raise Pyr4tRuntimeError(
            f"[{r.status_code}] GitHub API error: {r.text}"
        )

    r.raise_for_status()
    repos = r.json()

    print_console = []
    for repo in repos:
        name = repo["name"]
        if name.startswith("pyr4t"):
            private = repo["private"]
            visibility = "PRIVATE" if private else "PUBLIC"

            print_console.append(f"> {name} ({visibility})")

            rel_url = f"https://api.github.com/repos/R4tL/{name}/releases"
            rr = requests.get(rel_url, headers=headers, timeout=10)

            if rr.status_code != 200:
                print_console.append("   └─ No releases or access denied")
                print("   └─ No releases or access denied")
                continue

            releases = rr.json()
            if not releases:
                print_console.append("   └─ No releases")
                continue

            for rel in releases:
                tag = rel["tag_name"]
                title = rel["name"] or tag
                print_console.append(f"   └─ {title}")
    if not print_console:
        print_console.append("[warning] No pyr4t package found.")
    print("\n".join(print_console))


def maj_token(token: str):
    """Update GitHub token used for private pyr4t package installation.

    Args:
        token (str): GitHub token
    
    Raises:
        Pyr4tRuntimeError: If the token is invalid or cannot be saved.
    """

    # Verify token
    headers = {}
    headers["Authorization"] = f"token {token}"
    url = "https://api.github.com/user/repos"
    r = requests.get(url, headers=headers, timeout=10)
    if r.status_code in (401, 403, 404):
        raise Pyr4tRuntimeError(
            f"[{r.status_code}] Invalid token: {r.text}"
        )
    elif r.status_code != 200:
        raise Pyr4tRuntimeError(
            f"[{r.status_code}] GitHub API error: {r.text}"
        )
    else:
        # Add token to keyring
        save_token(token)
        token_saved = load_token()
        if token_saved != token:
            raise Pyr4tRuntimeError("Failed to save token securely.")
        print("[info] Token saved securely in system keyring.")


def save_token(token: str):
    """Save GitHub token securely in system keyring.

    Args:
        token (str): GitHub token
    """
    keyring.set_password("pyr4t", "github_token", token)


def load_token() -> str | None:
    """Load GitHub token from system keyring.

    Returns:
        str | None: GitHub token if found, else None
    """
    return keyring.get_password("pyr4t", "github_token")
