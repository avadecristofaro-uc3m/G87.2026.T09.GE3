"""Module for managing the Json Projects store"""
from uc3m_consulting.json_storage.JsonStore import JsonStore
from uc3m_consulting.enterprise_manager_config import PROJECTS_STORE_FILE


class ProjectsJsonStore(JsonStore):
    """Handles persistence of projects"""

    def load(self):
        """Load all projects"""
        return super().load_json_file(PROJECTS_STORE_FILE)

    def save(self, projects_list):
        """Save all projects"""
        super().save_json_file(PROJECTS_STORE_FILE, projects_list)

    def add(self, new_project: dict):
        """Add a new project and persist"""
        projects = self.load()
        projects.append(new_project)
        self.save(projects)
