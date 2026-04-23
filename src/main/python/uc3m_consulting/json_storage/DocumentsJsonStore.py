"""Module for managing the Json Documents store"""

from uc3m_consulting.enterprise_management_exception import EnterpriseManagementException
from uc3m_consulting.json_storage.JsonStore import JsonStore
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

    def add_to_store(self, new_document: dict):
        """Add a new document after duplicate validation and persist"""
        super().add_to_store(new_document)

    def save_documents(self, documents_list):
        """Replace all documents and persist"""
        self._data_list = documents_list
        self.save()
