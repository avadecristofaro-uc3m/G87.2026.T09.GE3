"""Module """
import re
import json

from datetime import datetime, timezone

from freezegun import freeze_time

from uc3m_consulting.attribute.query_date_attribute import QueryDateAttribute
from uc3m_consulting.enterprise_project import EnterpriseProject
from uc3m_consulting.enterprise_management_exception import EnterpriseManagementException
from uc3m_consulting.enterprise_manager_config import (PROJECTS_STORE_FILE,
                                                       TEST_DOCUMENTS_STORE_FILE,
                                                       TEST_NUMDOCS_STORE_FILE)
from uc3m_consulting.json_storage.JsonStore import JsonStore
from uc3m_consulting.json_storage.ProjectsJsonStore import ProjectsJsonStore
from uc3m_consulting.project_document import ProjectDocument
from uc3m_consulting.attribute.cif_attribute import CifAttribute
from uc3m_consulting.attribute.acronym_attribute import AcronymAttribute
from uc3m_consulting.attribute.description_attribute import DescriptionAttribute
from uc3m_consulting.attribute.department_attribute import DepartmentAttribute
from uc3m_consulting.attribute.date_attribute import DateAttribute
from uc3m_consulting.attribute.budget_attribute import BudgetAttribute

class EnterpriseManager:
    class __EnterpriseManager:
        """Class for providing the methods for managing the orders"""
        def __init__(self):
            pass

        #pylint: disable=too-many-arguments, too-many-positional-arguments
        def register_project(self,
                             company_cif: str,
                             project_acronym: str,
                             project_description: str,
                             department: str,
                             date: str,
                             budget: str):
            """registers a new project"""
            validated_cif = CifAttribute(company_cif)
            validated_acronym = AcronymAttribute(project_acronym).value
            validated_description = DescriptionAttribute(project_description).value
            validated_department = DepartmentAttribute(department).value
            validated_date = DateAttribute(date).value
            validated_budget = BudgetAttribute(budget).value

            new_project = EnterpriseProject(company_cif=validated_cif.attr_value,
                                            project_acronym=validated_acronym,
                                            project_description=validated_description,
                                            department=validated_department,
                                            starting_date=validated_date,
                                            project_budget=validated_budget)

            projects_store = ProjectsJsonStore()
            # projects_list = projects_store.load()
            project_data = new_project.to_json()
            # projects_store.raise_if_duplicate(projects_list, project_data,
            #                          "Duplicated project in projects list")
            projects_store.add_to_store(project_data)

            return new_project.project_id


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
            validated_date = QueryDateAttribute(date_str).value

            # open documents
            json_store = JsonStore()
            documents_list = json_store.load_json_file()

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

            docs_report_list = json_store.load_json_file(TEST_NUMDOCS_STORE_FILE)
            docs_report_list.append(report)
            json_store.save_json_file(TEST_NUMDOCS_STORE_FILE, docs_report_list)

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

    instance = None

    def __new__(cls, *args, **kwargs):
        if cls.instance is None:
            cls.instance = cls.__EnterpriseManager()
        return cls.instance

    def __getattr__(self, name):
        return getattr(self.instance, name)

    def __setattr__(self, name, value):
        return setattr(self.instance, name, value)