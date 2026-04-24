"""Module for managing the Json Documents store"""

from uc3m_consulting.json_storage.json_store import JsonStore
from uc3m_consulting.enterprise_manager_config import TEST_DOCUMENTS_STORE_FILE


class DocumentsJsonStore(JsonStore):
    """Handles persistence of documents"""

    _FILE_PATH = TEST_DOCUMENTS_STORE_FILE

    def load(self):
        """Load documents"""
        return super().load_json_file()

    def save(self):
        """Save all documents"""
        super().save_json_file()

    def save_documents(self, documents_list):
        """Replace all documents and persist"""
        self._data_list = documents_list
        self.save()
