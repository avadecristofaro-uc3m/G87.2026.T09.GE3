"""Module"""
from unittest import TestCase
from uc3m_consulting import EnterpriseManager
from uc3m_consulting.json_storage.projects_json_store import ProjectsJsonStore
from uc3m_consulting.json_storage.documents_json_store import DocumentsJsonStore

class SingletonTest(TestCase):
    """Class for dealing with Singletons"""
    def test_enterprise_manager_singleton(self):
        """Validate that enterprise manager class is instantiated as a Singleton"""
        enterprise_manager1 = EnterpriseManager()
        enterprise_manager2 = EnterpriseManager()
        enterprise_manager3 = EnterpriseManager()
        self.assertEqual(enterprise_manager1, enterprise_manager2)  # assert instances are the same
        self.assertEqual(enterprise_manager2, enterprise_manager3)  # assert instances are the same

    def test_projects_json_store_singleton(self):
        """Validate that projects JSON store class is instantiated as a Singleton"""
        projects_store1 = ProjectsJsonStore()
        projects_store2 = ProjectsJsonStore()
        projects_store3 = ProjectsJsonStore()
        self.assertEqual(projects_store1, projects_store2)
        self.assertEqual(projects_store2, projects_store3)

    def test_documents_json_store_singleton(self):
        """Validate that documents JSON store class is instantiated as a Singleton"""
        documents_store1 = DocumentsJsonStore()
        documents_store2 = DocumentsJsonStore()
        documents_store3 = DocumentsJsonStore()
        self.assertEqual(documents_store1, documents_store2)
        self.assertEqual(documents_store2, documents_store3)

# if __name__ == '__main__':
#     unittest.main()
