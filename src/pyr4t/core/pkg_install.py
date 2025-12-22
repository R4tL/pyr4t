"""Functions to manage pyr4t packges."""

import platform
import subprocess
import sys
import tempfile
import os
import shutil
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
            "https://api.github.com/repos/R4tL/"
            f"{package}/releases/tags/v{version}"
        )
    else:
        url = f"https://api.github.com/repos/R4tL/{package}/releases/latest"

    headers = {}
    response = requests.get(url, timeout=5)
    github_token = os.getenv("GITHUB_TOKEN")

    # Token management
    if response.status_code in (401, 403, 404):  # need token / not found (nf)
        need_token = False
        if github_token:
            headers["Authorization"] = f"token {github_token}"
            response = requests.get(url, headers=headers, timeout=5)
            if response.status_code in (401, 403, 404):
                need_token = True
        else:
            need_token = True
        if need_token:
            need_input_tok = False
            token_file = Path().home() / ".pyr4t" / "token"
            if token_file.exists():
                with open(token_file, "r", encoding="utf-8") as f:
                    token = f.read()
                headers["Authorization"] = f"token {token}"
                response = requests.get(url, headers=headers, timeout=5)
                if response.status_code in (401, 403, 404):  # invalid / nf
                    need_input_tok = True
            else:
                need_input_tok = True
            if need_input_tok:
                token = input("Token: ")
                headers["Authorization"] = f"token {token}"
                response = requests.get(url, headers=headers, timeout=5)
                if response.status_code in (401, 403, 404):  # invalid / nf
                    raise RuntimeError(
                        f"[{response.status_code}] Invalid token "
                        f"or package name: {response.text}"
                    )
                with open(token_file, "w", encoding="utf-8") as f:
                    f.write(token)
                print(f"[info] Token added in {token_file}")
    if response.status_code != 200:
        raise RuntimeError(
            f"[{response.status_code}] GitHub API: {response.text}"
        )

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

    # download_url = asset["browser_download_url"]
    download_url = asset["url"]
    headers["Accept"] = "application/octet-stream"
    print(f"[info] Downloading {asset['name']} from {download_url} ...")

    # DL tmp file
    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_file = Path(tmp_dir) / str(asset['name'])
        with requests.get(
            download_url, headers=headers, stream=True, timeout=10
        ) as r:
            r.raise_for_status()
            with open(tmp_file, "wb") as f:
                shutil.copyfileobj(r.raw, f)
        # DL with pip
        print("[info] Installing with pip ...")
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", str(tmp_file)]
        )

    print(f"[info] Installation of {package} finished")

# TODO :
# - prendre que ceux qui commencent par pyr4t-
# - afficher tout d'uncoup (car ya un chargement avec les requetes)
def install_info(show_private: bool = False):
    """
    Print information about avalible pyr4t packages.
    Args:
        show_private (bool, optional): Show private repositories.
    """

    print("[info] Fetching pyr4t package list from"
          " GitHub (can take a while)...")

    headers = {}

    # URL depending on mode
    if show_private:
        url = "https://api.github.com/user/repos"
    else:
        url = "https://api.github.com/users/R4tL/repos"

    # First attempt (no token)
    r = requests.get(url, headers=headers, timeout=10)

    # Token management
    if show_private and r.status_code in (401, 403, 404):
        need_token = False
        github_token = os.getenv("GITHUB_TOKEN")

        if github_token:
            headers["Authorization"] = f"token {github_token}"
            r = requests.get(url, headers=headers, timeout=10)
            if r.status_code in (401, 403, 404):
                need_token = True
        else:
            need_token = True

        if need_token:
            need_input_tok = False
            token_file = Path.home() / ".pyr4t" / "token"

            if token_file.exists():
                token = token_file.read_text(encoding="utf-8").strip()
                headers["Authorization"] = f"token {token}"
                r = requests.get(url, headers=headers, timeout=10)
                if r.status_code in (401, 403, 404):
                    need_input_tok = True
            else:
                need_input_tok = True

            if need_input_tok:
                token = input("Token: ").strip()
                headers["Authorization"] = f"token {token}"
                r = requests.get(url, headers=headers, timeout=10)

                if r.status_code in (401, 403, 404):
                    raise RuntimeError(
                        f"[{r.status_code}] Invalid token: {r.text}"
                    )

                token_file.parent.mkdir(parents=True, exist_ok=True)
                token_file.write_text(token, encoding="utf-8")
                print(f"[info] Token added in {token_file}")

    if r.status_code != 200:
        raise RuntimeError(f"[{r.status_code}] GitHub API: {r.text}")

    r.raise_for_status()
    repos = r.json()

    print_console = []
    for repo in repos:
        name = repo["name"]
        if name.startswith("pyr4t"):
            private = repo["private"]
            visibility = "PRIVATE" if private else "PUBLIC"

            print_console.append(f"{name} ({visibility})")

            rel_url = f"https://api.github.com/repos/R4tL/{name}/releases"
            rr = requests.get(rel_url, headers=headers, timeout=10)

            if rr.status_code != 200:
                print_console.append("  └─ No releases or access denied")
                print("  └─ No releases or access denied")
                continue

            releases = rr.json()
            if not releases:
                print_console.append("  └─ No releases")
                continue

            for rel in releases:
                tag = rel["tag_name"]
                title = rel["name"] or tag
                print_console.append(f"  └─ {title}")

    print("\n".join(print_console))
