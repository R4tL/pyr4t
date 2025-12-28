"""Module for managing the projects database."""

from pathlib import Path

from pyr4t.models import Project
from pyr4t.utils import _JSONDBM4nager


class ProjectDBM4nager(_JSONDBM4nager[Project]):
    """
    Manages projects: add, list, update, select, and remove projects
    stored in a JSON file.
    """

    def __init__(self):
        super().__init__(Path.home() / ".pyr4t" / "projects.json")

    def add(self, title: str, path: str, version: str):
        """
        Adds a new project.
        Args:
            title (str): unique identifier for the project
            path (str): name of the user
            version (str): project version
        """

        path = str(Path(path).resolve())
        project: Project = {"path": path, "version": version}
        self.update_data(title, "add", project)
        if not (Path(path)).exists():
            print(f"[warning] Path does not exist: {path}")
        print(f"[info] Project added: {title}: {path} <v{version}>")

    def list(self) -> dict[str, Project]:
        """
        Lists all projects.
        Returns:
            dict[str, Project]: dictionary of project titles
                to Project objects
        """

        return self.listd

    def remove(self, title: str):
        """
        Removes a user project by title.
        Args:
            title (str): title of the project to remove
        """

        self.update_data(title, "rm")
        if title == "*":
            print("[info] All projects removed")
        else:
            print(f"[info] Project removed: {title}")

    def modify(self, title: str, path: str = None, version: str = None):
        """
        Updates an existing user project.
        Args:
            title (str): The title of the project to update.
            path (str, optional): new path for the project
            version (str): project version
        """

        project = self.listd.get(title)
        if path:
            project["path"] = path
        if version:
            project["version"] = version
        self.update_data(title, "updt", project)
        print(
            f"[info] Project updated: {title}: {project.get("path", "")} "
            f"<v{project.get("version", "")}>"
        )

    def switch(self, title: str):
        """
        Selects a project as the default project ('me').
        Args:
            title (str): title of the project to set as default
        """

        self.update_data(title, "slct")
        print(f"[info] Default project selected: {title}")

    def info(self) -> tuple[str, Project]:
        """
        Returns the title and project information ofthe current project.
        Returns:
            tuple[str, Project]: title and project data of the default project
        """

        return self.get_current()
