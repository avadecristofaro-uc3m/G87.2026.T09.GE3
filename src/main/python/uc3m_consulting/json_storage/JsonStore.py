"""Module for managing the JSON storage classes"""

import json
from uc3m_consulting.enterprise_management_exception import EnterpriseManagementException
class JsonStore:
    """Class for managing the JSON storage"""
    def __init__(self):
        pass

    def load_json_file(self, file_path):
        """Loads data from json file"""
        try:
            with open(file_path, "r", encoding="utf-8", newline="") as file:
                data_list = json.load(file)
        except FileNotFoundError:
            data_list = []
        except json.JSONDecodeError as exception:
            raise EnterpriseManagementException("JSON Decode Error - Wrong JSON Format") from exception
        return data_list