"""Module for managing the Json Number of Documents store"""

from uc3m_consulting.json_storage.json_store import JsonStore
from uc3m_consulting.enterprise_manager_config import TEST_NUMDOCS_STORE_FILE

class NumDocsJsonStore:
    """Singleton JSON store for document count reports."""


    class _NumDocsJsonStore(JsonStore):
        """Handles persistence of document count reports"""

        _FILE_PATH = TEST_NUMDOCS_STORE_FILE

        def load(self):
            """Load reports"""
            return super().load_json_file()

        def save(self):
            """Save all reports"""
            super().save_json_file()

        def save_reports(self, reports_list):
            """Replace all reports and persist"""
            self._data_list = reports_list
            self.save()

    __instance = None

    def __new__(cls):
        if not NumDocsJsonStore.__instance:
            NumDocsJsonStore.__instance = NumDocsJsonStore._NumDocsJsonStore()
        return NumDocsJsonStore.__instance

    def add_to_store(self, new_item: dict):
        """Add a new report to the store."""
        return self.__instance.add_to_store(new_item)
