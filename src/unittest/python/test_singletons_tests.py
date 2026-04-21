"""Module"""
from unittest import TestCase
from uc3m_consulting import EnterpriseManager


class SingletonTest(TestCase):
    """Class for dealing with Singletons"""
    def test_enterprise_manager_singleton(self):
        """Validate that enterprise manager class is instantiated as a Singleton"""
        enterprise_manager1 = EnterpriseManager()
        enterprise_manager2 = EnterpriseManager()
        enterprise_manager3 = EnterpriseManager()
        self.assertEqual(enterprise_manager1, enterprise_manager2)  # assert instances are the same
        self.assertEqual(enterprise_manager2, enterprise_manager3)  # assert instances are the same


# if __name__ == '__main__':
#     unittest.main()
