"""Module """
import re
import json

from datetime import datetime, timezone

from freezegun import freeze_time
from uc3m_consulting.enterprise_project import EnterpriseProject
from uc3m_consulting.enterprise_management_exception import EnterpriseManagementException
from uc3m_consulting.enterprise_manager_config import (PROJECTS_STORE_FILE,
                                                       TEST_DOCUMENTS_STORE_FILE,
                                                       TEST_NUMDOCS_STORE_FILE)
from uc3m_consulting.project_document import ProjectDocument
from uc3m_consulting.attribute.cif_attribute import cif_attribute
from uc3m_consulting.attribute.acronym_attribute import acronym_attribute
from uc3m_consulting.attribute.description_attribute import description_attribute
from uc3m_consulting.attribute.department_attribute import department_attribute
from uc3m_consulting.attribute.date_attribute import date_attribute

class EnterpriseManager:
    class __EnterpriseManager:
        """Class for providing the methods for managing the orders"""
        def __init__(self):
            pass


        def validate_starting_date(self, t_d):
            """validates the  date format  using regex"""
            my_date = self._validate_and_parse_date(t_d)

            if my_date < datetime.now(timezone.utc).date():
                raise EnterpriseManagementException("Project's date must be today or later.")

            if my_date.year < 2025 or my_date.year > 2050:
                raise EnterpriseManagementException("Invalid date format")
            return t_d
        #pylint: disable=too-many-arguments, too-many-positional-arguments
        def register_project(self,
                             company_cif: str,
                             project_acronym: str,
                             project_description: str,
                             department: str,
                             date: str,
                             budget: str):
            """registers a new project"""
            validated_cif = cif_attribute(company_cif)
            validated_acronym = acronym_attribute(project_acronym).value
            validated_description = description_attribute(project_description).value
            validated_department = department_attribute(department).value
            validated_date = date_attribute(date).value
            self._validate_budget(budget)


            new_project = EnterpriseProject(company_cif=validated_cif.attr_value,
                                            project_acronym=validated_acronym,
                                            project_description=validated_description,
                                            department=validated_department,
                                            starting_date=validated_date,
                                            project_budget=budget)

            projects_list = self._load_json_file(PROJECTS_STORE_FILE)

            project_data = new_project.to_json()
            self._raise_if_duplicate(projects_list, project_data, "Duplicated project in projects list")

            projects_list.append(project_data)

            self._save_json_file(PROJECTS_STORE_FILE, projects_list)

            return new_project.project_id

        @staticmethod
        def _validate_budget(budget: str) -> float:
            """Validate budget format and range, and return it as float."""
            try:
                budget_value = float(budget)
            except ValueError as exc:
                raise EnterpriseManagementException("Invalid budget amount") from exc

            budget_as_string = str(budget_value)
            if "." in budget_as_string:
                decimals_length = len(budget_as_string.split('.')[1])
                if decimals_length > 2:
                    raise EnterpriseManagementException("Invalid budget amount")

            if budget_value < 50000 or budget_value > 1000000:
                raise EnterpriseManagementException("Invalid budget amount")

            return budget_value
        @staticmethod
        def _raise_if_duplicate(projects, new_project, error_message: str):
            """Raises exception if duplicate project exists"""
            for project in projects:
                if project == new_project:
                    raise EnterpriseManagementException(error_message)

        def find_docs(self, date_str):
            """
            Generates a JSON report counting valid documents for a specific date.

            Checks cryptographic hashes and timestamps to ensure historical data integrity.
            Saves the output to 'resultado.json'.

            Args:
                date_str (str): date to query.

            Returns:
                number of documents found if report is successfully generated and saved.

            Raises:
                EnterpriseManagementException: On invalid date, file IO errors,
                    missing data, or cryptographic integrity failure.
            """
            self._validate_and_parse_date(date_str)

            # open documents
            documents_list = self._load_json_file(TEST_DOCUMENTS_STORE_FILE)

            documents_found_count = 0

            # loop to find
            for doc_entry in documents_list:
                time_val = doc_entry["register_date"]

                # string conversion for easy match
                doc_date_str = datetime.fromtimestamp(time_val).strftime("%d/%m/%Y")

                if doc_date_str == date_str:
                    if self._has_valid_document_signature(doc_entry):
                        documents_found_count = documents_found_count + 1
                    else:
                        raise EnterpriseManagementException("Inconsistent document signature")

            if documents_found_count == 0:
                raise EnterpriseManagementException("No documents found")

            # prepare json text
            report = self._create_docs_report(date_str, documents_found_count)

            docs_report_list = self._load_json_file(TEST_NUMDOCS_STORE_FILE)
            docs_report_list.append(report)
            self._save_json_file(TEST_NUMDOCS_STORE_FILE, docs_report_list)

            return documents_found_count

        @staticmethod
        def _create_docs_report(query_date: str, num_files: int) -> dict:
            """Create the report record for a document query."""
            current_timestamp = datetime.now(timezone.utc).timestamp()
            report_record = {"Querydate": query_date,
                 "ReportDate": current_timestamp,
                 "Numfiles": num_files
                 }
            return report_record

        @staticmethod
        def _has_valid_document_signature(el: dict) -> bool:
            """Returns true if the stored document signature is valid"""
            register_timestamp = el["register_date"]
            document_datetime = datetime.fromtimestamp(register_timestamp, tz=timezone.utc)
            with freeze_time(document_datetime):
                # check the project id (thanks to freezetime)
                # if project_id are different then the data has been
                # manipulated
                project_document = ProjectDocument(el["project_id"], el["file_name"])

                return project_document.document_signature == el["document_signature"]

        @staticmethod
        def _save_json_file(file_path, data_list):
            """Saves data to json file"""
            try:
                with open(file_path, "w", encoding="utf-8", newline="") as file:
                    json.dump(data_list, file, indent=2)
            except FileNotFoundError as exception:
                raise EnterpriseManagementException("Wrong file  or file path") from exception
            except json.JSONDecodeError as exception:
                raise EnterpriseManagementException("JSON Decode Error - Wrong JSON Format") from exception

        @staticmethod
        def _load_json_file(file_path):
            """Loads data from json file"""
            try:
                with open(file_path, "r", encoding="utf-8", newline="") as file:
                    data_list = json.load(file)
            except FileNotFoundError:
                data_list = []
            except json.JSONDecodeError as exception:
                raise EnterpriseManagementException("JSON Decode Error - Wrong JSON Format") from exception
            return data_list

        @staticmethod
        def _validate_and_parse_date(date_str: str):
            """Validate DD/MM/YYYY and return a date object"""
            EnterpriseManager.__EnterpriseManager._validate_field(
                r"^(([0-2]\d|3[0-1])\/(0\d|1[0-2])\/\d\d\d\d)$",
                date_str,
                "Invalid date format")

            try:
                my_date = datetime.strptime(date_str, "%d/%m/%Y").date()
            except ValueError as exception:
                raise EnterpriseManagementException("Invalid date format") from exception
            return my_date

    instance = None

    def __new__(cls, *args, **kwargs):
        if cls.instance is None:
            cls.instance = cls.__EnterpriseManager()
        return cls.instance

    def __getattr__(self, name):
        return getattr(self.instance, name)

    def __setattr__(self, name, value):
        return setattr(self.instance, name, value)