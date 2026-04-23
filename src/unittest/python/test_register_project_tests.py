"""class for testing the regsiter_project method"""
import unittest
import csv
import json
import os.path
import hashlib
from unittest import TestCase
from os import remove
from freezegun import freeze_time
from uc3m_consulting import (JSON_FILES_PATH,
                        PROJECTS_STORE_FILE,
                        EnterpriseProject,
                        EnterpriseManager,
                        EnterpriseManagementException)

class TestRegisterProjectTest(TestCase):
    """Class for testing register_project"""

    def setUp(self):
        """ inicializo document_entry entorno de prueba """
        if os.path.exists(PROJECTS_STORE_FILE):
            remove(PROJECTS_STORE_FILE)


    @staticmethod
    def read_file():
        """ this method read a Json file and return the value """
        my_file= PROJECTS_STORE_FILE
        try:
            with open(my_file, "r", encoding="utf-8", newline="") as file:
                data = json.load(file)
        except FileNotFoundError as ex:
            raise EnterpriseManagementException("Wrong file or file path") from ex
        except json.JSONDecodeError as ex:
            raise EnterpriseManagementException("JSON Decode Error - Wrong JSON Format") from ex
        return data

    #pylint: disable=too-many-locals
    @freeze_time("2024/12/31 13:00:00")
    def test_parametrized_cases_tests(self):
        """Parametrized cases read from testingCases_RF1.csv"""
        my_cases = JSON_FILES_PATH + "test_cases_2026_method1.csv"
        with open(my_cases, newline='', encoding='utf-8') as csvfile:
            param_test_cases = csv.DictReader(csvfile, delimiter=';')
            mngr = EnterpriseManager()
            for row in param_test_cases:
                test_id = row['ID_TEST']
                enterprise_cif = row["CIF"]
                project_acronym = row["ACRONYM"]
                project_department = row["DEPARTMENT"]
                project_budget = row["BUDGET"]
                try:
                    number_budget = float(project_budget)
                except ValueError:
                    number_budget = row["BUDGET"]
                result = row["RESULT"]
                valid = row["VALID"]
                project_date = row["STARTING_DATE"]
                project_description = row["DESCRIPTION"]

                if valid == "VALID":
                    with self.subTest(test_id + valid):
                        valor = mngr.register_project(company_cif=enterprise_cif,
                                                      project_acronym=project_acronym,
                                                      department=project_department,
                                                      budget=number_budget,
                                                      date=project_date,
                                                      project_description=project_description)
                        self.assertEqual(result, valor)
                        # Check if this DNI is store in storeRequest.json
                        my_data = self.read_file()
                        my_request = EnterpriseProject(company_cif=enterprise_cif,
                                                     project_acronym=project_acronym,
                                                     project_description=project_description,
                                                     starting_date=project_date,
                                                     project_budget=number_budget,
                                                     department=project_department)
                        found = False
                        for k in my_data:
                            if k["project_id"] == valor:
                                found = True
                                # this assert give me more information
                                # about the differences than assertEqual
                                self.assertDictEqual(k, my_request.to_json())
                        # if found is False , this assert fails
                        self.assertTrue(found)
                else:
                    with self.subTest(test_id + valid):

                        # we calculater the files signature bejore calling the tested method
                        if os.path.isfile(PROJECTS_STORE_FILE):
                            with open(PROJECTS_STORE_FILE, "r",
                                      encoding="utf-8", newline="") as file_org:
                                hash_original = hashlib.md5(str(file_org).encode()).hexdigest()
                        else:
                            hash_original = ""
                        with self.assertRaises(EnterpriseManagementException) as c_m:
                            valor = mngr.register_project(company_cif=enterprise_cif,
                                                          project_acronym=project_acronym,
                                                          department=project_department,
                                                          budget=number_budget,
                                                          date=project_date,
                                                          project_description=project_description)
                        self.assertEqual(c_m.exception.message, result)

                        # now we check that the signature of the file is the same
                        # (the file didn't change)
                        if os.path.isfile(PROJECTS_STORE_FILE):
                            with open(PROJECTS_STORE_FILE, "r",
                                      encoding="utf-8", newline="") as file:
                                hash_new = hashlib.md5(str(file).encode()).hexdigest()
                        else:
                            hash_new = ""
                        self.assertEqual(hash_new, hash_original)

    @freeze_time("2026/03/22 13:00:00")
    def test_duplicated_project_test(self):

        """tets method for duplicated projects"""

        enterprise_cif = "A12345674"
        project_acronym = "TEST5"
        project_department = "HR"
        project_date = "22/03/2026"
        project_description = "Testing duplicated projects"
        number_budget = 50000.00

        mngr  = EnterpriseManager()
        mngr.register_project(company_cif=enterprise_cif,
                                           project_acronym=project_acronym,
                                           project_description=project_description,
                                           date=project_date,
                                           budget=number_budget,
                                           department=project_department)
        if os.path.isfile(PROJECTS_STORE_FILE):
            with open(PROJECTS_STORE_FILE, "r", encoding="utf-8", newline="") as file_org:
                hash_original = hashlib.md5(str(file_org).encode()).hexdigest()
        else:
            hash_original = ""
        with self.assertRaises(EnterpriseManagementException) as c_m:
            mngr.register_project(company_cif=enterprise_cif,
                                               project_acronym=project_acronym,
                                               project_description=project_description,
                                               date=project_date,
                                               budget=number_budget,
                                               department=project_department)
        self.assertEqual(c_m.exception.message, "Duplicated project in projects list")

        # now we check that the signature of the file is the same
        # (the file didn't change)
        if os.path.isfile(PROJECTS_STORE_FILE):
            with open(PROJECTS_STORE_FILE, "r", encoding="utf-8", newline="") as file:
                hash_new = hashlib.md5(str(file).encode()).hexdigest()
        else:
            hash_new = ""
        self.assertEqual(hash_new, hash_original)

    @freeze_time("2026/03/22 13:00:00")
    def test_project_for_today(self):
        """test for a project today (using freezetime)"""
        enterprise_cif = "A12345674"
        project_acronym = "TEST5"
        project_department = "HR"
        project_date = "22/03/2026"
        project_description = "Testing today's project"
        number_budget = 50000.00
        mngr = EnterpriseManager()
        my_request = mngr.register_project(company_cif=enterprise_cif,
                                           project_acronym=project_acronym,
                                           project_description=project_description,
                                           date=project_date,
                                           budget=number_budget,
                                           department=project_department)
        self.assertEqual("6ad10748f3c9137c0f22ff7d4eed8d19",my_request)
        my_data = self.read_file()
        my_project = EnterpriseProject(company_cif=enterprise_cif,
                                       project_acronym=project_acronym,
                                       project_description=project_description,
                                       starting_date=project_date,
                                       project_budget=number_budget,
                                       department=project_department)
        found = False
        for k in my_data:
            if k["project_id"] == my_request:
                found = True
                # this assert give me more information
                # about the differences than assertEqual
                self.assertDictEqual(k, my_project.to_json())
        # if found is False , this assert fails
        self.assertTrue(found)

    @freeze_time("2025/03/22 13:00:00")
    def test_project_for_tomorrow(self):
        """test for a tomorrow's project (using freezetime)"""
        enterprise_cif = "A12345674"
        project_acronym = "TEST5"
        project_department = "HR"
        project_date = "23/03/2026"
        project_description = "Testing tomorrow's project"
        number_budget = 50000.00
        mngr = EnterpriseManager()
        my_request = mngr.register_project(company_cif=enterprise_cif,
                                           project_acronym=project_acronym,
                                           project_description=project_description,
                                           date=project_date,
                                           budget=number_budget,
                                           department=project_department)
        self.assertEqual("8aab556991e7b0f1361b72e3ab17fa81", my_request)
        my_data = self.read_file()
        my_project = EnterpriseProject(company_cif=enterprise_cif,
                                       project_acronym=project_acronym,
                                       project_description=project_description,
                                       starting_date=project_date,
                                       project_budget=number_budget,
                                       department=project_department)
        found = False
        for k in my_data:
            if k["project_id"] == my_request:
                found = True
                # this assert give me more information
                # about the differences than assertEqual
                self.assertDictEqual(k, my_project.to_json())
        # if found is False , this assert fails
        self.assertTrue(found)

    @freeze_time("2026/03/26 13:00:00")
    def test_project_yesterday_test(self):
        """test for a yesterday's project (using freezetime)"""
        enterprise_cif = "A12345674"
        project_acronym = "TEST5"
        project_department = "HR"
        project_date = "23/03/2026"
        project_description = "Testing yesteday's project"
        number_budget = 50000.00
        mngr = EnterpriseManager()
        # enterprise_cif;project_acronym;project_department;project_date;project_description;number_budget;RESULT

        if os.path.isfile(PROJECTS_STORE_FILE):
            with open(PROJECTS_STORE_FILE, "r", encoding="utf-8", newline="") as file_org:
                hash_original = hashlib.md5(str(file_org).encode()).hexdigest()
        else:
            hash_original = ""
        with self.assertRaises(EnterpriseManagementException) as c_m:
            mngr.register_project(company_cif=enterprise_cif,
                                               project_acronym=project_acronym,
                                               project_description=project_description,
                                               date=project_date,
                                               budget=number_budget,
                                               department=project_department)
        self.assertEqual(c_m.exception.message, "Project's date must be today or later.")

        # now we check that the signature of the file is the same
        # (the file didn't change)
        if os.path.isfile(PROJECTS_STORE_FILE):
            with open(PROJECTS_STORE_FILE, "r", encoding="utf-8", newline="") as file:
                hash_new = hashlib.md5(str(file).encode()).hexdigest()
        else:
            hash_new = ""
        self.assertEqual(hash_new, hash_original)


if __name__ == '__main__':
    unittest.main()
