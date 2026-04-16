"""Global constants for finding the path"""
import os.path
JSON_FILES_PATH = os.path.join(os.path.dirname(__file__),"../../../unittest/json_files/")
JSON_FILES_TRANSACTIONS = JSON_FILES_PATH + ("/transactions/")
PROJECTS_STORE_FILE = JSON_FILES_PATH + "projects_store.json"
DOCUMENTS_STORE_FILE = JSON_FILES_PATH + "documents_store.json"
TRANSACTIONS_STORE_FILE = JSON_FILES_PATH + "transactions.json"
BALANCES_STORE_FILE = JSON_FILES_PATH + "balances.json"
#CONSTANTS FOR TESTING FILES WITH DATA FOR
# PROJECTS AND DOCUMENTS ONLY FOR TESTING
TEST_DOCUMENTS_STORE_FILE = JSON_FILES_PATH + "test_documents_store.json"
TEST_PROJECTS_STORE_FILE = JSON_FILES_PATH + "test_projects_store.json"
TEST_NUMDOCS_STORE_FILE = JSON_FILES_PATH + "test_numdocs_store.json"
