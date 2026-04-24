"""Module for managing the Json Projects store"""


from uc3m_consulting.enterprise_management_exception import EnterpriseManagementException
from uc3m_consulting.json_storage.json_store import JsonStore
from uc3m_consulting.enterprise_manager_config import PROJECTS_STORE_FILE

class ProjectsJsonStore:
    """Singleton projects JSON store"""

    class _ProjectsJsonStore(JsonStore):
        """Handles persistence of projects"""
        _FILE_PATH = PROJECTS_STORE_FILE

        def load(self):
            """Load projects"""
            return super().load_json_file()

        def save(self):
            """Save all projects"""
            super().save_json_file()

        def add_to_store(self, new_item: dict):
            """Add a new project after duplicate validation and persist"""
            projects = self.load()
            self.raise_if_duplicate(projects, new_item, "Duplicated project in projects list")
            projects.append(new_item)
            self.save()

        @staticmethod
        def raise_if_duplicate(projects, new_project, error_message: str):
            """Raises exception if duplicate project exists"""
            for project in projects:
                if project == new_project:
                    raise EnterpriseManagementException(error_message)

        def save_projects(self, projects_list):
            """Replace all projects and persist"""
            self._data_list = projects_list
            self.save()

    __instance = None

    def __new__(cls):
        if not ProjectsJsonStore.__instance:
            ProjectsJsonStore.__instance = ProjectsJsonStore._ProjectsJsonStore()
        return ProjectsJsonStore.__instance

    def add_to_store(self, new_project: dict):
        """Add a new project to the store."""
        return self.__instance.add_to_store(new_project)