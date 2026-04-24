"""Module for managing the JSON storage classes"""

import json
from uc3m_consulting.enterprise_management_exception import EnterpriseManagementException
class JsonStore:
    """Super class for managing the JSON files"""
    _FILE_PATH = ""

    def __init__(self):
        self._data_list = []
        self.load_json_file()

    def load_json_file(self):
        """Loads data from json file"""

        try:
            with open(self._FILE_PATH, "r", encoding="utf-8", newline="") as file:
                self._data_list = json.load(file)
        except FileNotFoundError:
            self._data_list = []
        except json.JSONDecodeError as exception:
            raise EnterpriseManagementException(
                "JSON Decode Error - Wrong JSON Format"
            ) from exception
        return self._data_list

    def save_json_file(self):
        """Saves data to json file"""
        try:
            with open(self._FILE_PATH, "w", encoding="utf-8", newline="") as file:
                json.dump(self._data_list, file, indent=2)
        except FileNotFoundError as exception:
            raise EnterpriseManagementException("Wrong file  or file path") from exception
        except json.JSONDecodeError as exception:
            raise EnterpriseManagementException(
                "JSON Decode Error - Wrong JSON Format"
            ) from exception

    def add_to_store(self, new_item: dict):
        """Appends item to data list"""
        self.load_json_file()
        self._data_list.append(new_item)
        self.save_json_file()
