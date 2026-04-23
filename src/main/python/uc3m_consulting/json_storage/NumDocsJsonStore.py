"""Module for managing the Json Number of Documents store"""

from uc3m_consulting.json_storage.JsonStore import JsonStore
from uc3m_consulting.enterprise_manager_config import TEST_NUMDOCS_STORE_FILE


class NumDocsJsonStore(JsonStore):
    """Handles persistence of document count reports"""

    _FILE_PATH = TEST_NUMDOCS_STORE_FILE

    def load(self):
        """Load reports"""
        return super().load_json_file()

    def save(self):
        """Save all reports"""
        super().save_json_file()

    def add_to_store(self, new_report: dict):
        """Add a new report and persist"""
        super().add_to_store(new_report)

    def save_reports(self, reports_list):
        """Replace all reports and persist"""
        self._data_list = reports_list
        self.save()
