"""
Core module for pyr4t.
This module provides essential classes and functions for project generation,
installation, and profile management.
"""

from .dev import cls, dstr, fmt, init, venv
from .dev import deploy as dev_deploy
from .dev import run as dev_run
from .package import install_pyr4tpackage, uninstall_pyr4tpackage
from .prod import build, deploy, run, test
from .project import ProjectArchM4nager, ProjectDBM4nager
from .user import UserDBM4nager

__all__ = [
    "ProjectArchM4nager",
    "UserDBM4nager",
    "ProjectDBM4nager",
    "install_pyr4tpackage",
    "uninstall_pyr4tpackage",
    "build",
    "deploy",
    "run",
    "test",
    "cls",
    "dstr",
    "fmt",
    "init",
    "venv",
    "dev_deploy",
    "dev_run",
]