"""Installer utilities for pyr4t packs."""

import subprocess
import sys


def pyr4t_install(name: str, version: str = "main", protocol: str = "https"):
    """
    Installs a pyr4t pack from a GitHub repository using pip.
    Args:
        name (str): Name of the pyr4t pack (GitHub repo).
        version (str, optional): Branch, tag, or commit to install. Defaults to "main".
        protocol (str, optional): Protocol to use for cloning. Defaults to "https".
    """

    if not name.startswith("pyr4t"):
        name = f"pyr4t{name}"
    link = f"git+{protocol}://github.com/R4tL/{name}.git@{version}"
    print(f"[info] Installing pyr4t pack {name}@{version} from {link}...")
    subprocess.run([sys.executable, "-m", "pip", "install", link], check=True)