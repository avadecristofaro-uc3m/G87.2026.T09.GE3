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

class EnterpriseManager:
    """Class for providing the methods for managing the orders"""
    def __init__(self):
        pass

    @staticmethod
    def validate_cif(c: str):
        """validates a cif number """
        if not isinstance(c, str):
            raise EnterpriseManagementException("CIF code must be a string")
        p = re.compile(r"^[ABCDEFGHJKNPQRSUVW]\d{7}[0-9A-J]$")
        if not p.fullmatch(c):
            raise EnterpriseManagementException("Invalid CIF format")

        l = c[0]
        n = c[1:8]
        u = c[8]

        s1 = 0
        s2 = 0

        for i in range(len(n)):
            if i % 2 == 0:
                x = int(n[i]) * 2
                if x > 9:
                    s1 = s1 + (x // 10) + (x % 10)
                else:
                    s1 = s1 + x
            else:
                s2 = s2 + int(n[i])

        t = s1 + s2
        u2 = t % 10
        r = 10 - u2

        if r == 10:
            r = 0

        dic = "JABCDEFGHI"

        if l in ('A', 'B', 'E', 'H'):
            if str(r) != u:
                raise EnterpriseManagementException("Invalid CIF character control number")
        elif l in ('P', 'Q', 'S', 'K'):
            if dic[r] != u:
                raise EnterpriseManagementException("Invalid CIF character control letter")
        else:
            raise EnterpriseManagementException("CIF type not supported")
        return True

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
        self.validate_cif(company_cif)
        mr = re.compile(r"^[a-zA-Z0-9]{5,10}")
        res = mr.fullmatch(project_acronym)
        if not res:
            raise EnterpriseManagementException("Invalid acronym")
        md = re.compile(r"^.{10,30}$")
        res = md.fullmatch(project_description)
        if not res:
            raise EnterpriseManagementException("Invalid description format")

        mr = re.compile(r"(HR|FINANCE|LEGAL|LOGISTICS)")
        res = mr.fullmatch(department)
        if not res:
            raise EnterpriseManagementException("Invalid department")

        self.validate_starting_date(date)

        try:
            f_bdgt  = float(budget)
        except ValueError as exc:
            raise EnterpriseManagementException("Invalid budget amount") from exc

        n_str = str(f_bdgt)
        if '.' in n_str:
            decimales = len(n_str.split('.')[1])
            if decimales > 2:
                raise EnterpriseManagementException("Invalid budget amount")

        if f_bdgt < 50000 or f_bdgt > 1000000:
            raise EnterpriseManagementException("Invalid budget amount")


        new_project = EnterpriseProject(company_cif=company_cif,
                                        project_acronym=project_acronym,
                                        project_description=project_description,
                                        department=department,
                                        starting_date=date,
                                        project_budget=budget)

        try:
            with open(PROJECTS_STORE_FILE, "r", encoding="utf-8", newline="") as file:
                t_l = json.load(file)
        except FileNotFoundError:
            t_l = []
        except json.JSONDecodeError as ex:
            raise EnterpriseManagementException("JSON Decode Error - Wrong JSON Format") from ex

        for t_i in t_l:
            if t_i == new_project.to_json():
                raise EnterpriseManagementException("Duplicated project in projects list")

        t_l.append(new_project.to_json())

        try:
            with open(PROJECTS_STORE_FILE, "w", encoding="utf-8", newline="") as file:
                json.dump(t_l, file, indent=2)
        except FileNotFoundError as ex:
            raise EnterpriseManagementException("Wrong file  or file path") from ex
        except json.JSONDecodeError as ex:
            raise EnterpriseManagementException("JSON Decode Error - Wrong JSON Format") from ex
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
        my_date = self._validate_and_parse_date(date_str)

        # open documents
        try:
            with open(TEST_DOCUMENTS_STORE_FILE, "r", encoding="utf-8", newline="") as file:
                d_list = json.load(file)
        except FileNotFoundError as ex:
            raise EnterpriseManagementException("Wrong file  or file path") from ex


        rst = 0

        # loop to find
        for el in d_list:
            time_val = el["register_date"]

            # string conversion for easy match
            doc_date_str = datetime.fromtimestamp(time_val).strftime("%d/%m/%Y")

            if doc_date_str == date_str:
                d_obj = datetime.fromtimestamp(time_val, tz=timezone.utc)
                with freeze_time(d_obj):
                    # check the project id (thanks to freezetime)
                    # if project_id are different then the data has been
                    #manipulated
                    p = ProjectDocument(el["project_id"], el["file_name"])
                    if p.document_signature == el["document_signature"]:
                        rst = rst + 1
                    else:
                        raise EnterpriseManagementException("Inconsistent document signature")

        if rst == 0:
            raise EnterpriseManagementException("No documents found")
        # prepare json text
        now_str = datetime.now(timezone.utc).timestamp()
        s = {"Querydate":  date_str,
             "ReportDate": now_str,
             "Numfiles": rst
             }

        try:
            with open(TEST_NUMDOCS_STORE_FILE, "r", encoding="utf-8", newline="") as file:
                dl = json.load(file)
        except FileNotFoundError:
            dl = []
        except json.JSONDecodeError as ex:
            raise EnterpriseManagementException("JSON Decode Error - Wrong JSON Format") from ex
        dl.append(s)
        try:
            with open(TEST_NUMDOCS_STORE_FILE, "w", encoding="utf-8", newline="") as file:
                json.dump(dl, file, indent=2)
        except FileNotFoundError as ex:
            raise EnterpriseManagementException("Wrong file  or file path") from ex
        return rst

    @staticmethod
    def _validate_and_parse_date(date_str: str):
        """Validate DD/MM/YYYY and return a date object"""
        mr = re.compile(r"^(([0-2]\d|3[0-1])\/(0\d|1[0-2])\/\d\d\d\d)$")
        res = mr.fullmatch(date_str)
        if not res:
            raise EnterpriseManagementException("Invalid date format")

        try:
            my_date = datetime.strptime(date_str, "%d/%m/%Y").date()
        except ValueError as ex:
            raise EnterpriseManagementException("Invalid date format") from ex
        return my_date
