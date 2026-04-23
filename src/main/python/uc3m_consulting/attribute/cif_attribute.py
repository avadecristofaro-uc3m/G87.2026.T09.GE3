"""Class for validating the CIF"""
import re
from uc3m_consulting.enterprise_management_exception import EnterpriseManagementException
from .attribute import Attribute

class CifAttribute(Attribute):
    """class for CIF attribute"""
    def __init__(self,attr_value):
        self.error_message = ""
        self.validation_pattern = r"^[ABCDEFGHJKNPQRSUVW]\d{7}[0-9A-J]$"
        self.attr_value = self.validate(attr_value)

    def validate(self,attr_value):
        """validates cif attribute"""
        if not isinstance(attr_value, str):
            self.error_message = "CIF code must be a string"
            raise EnterpriseManagementException(self.error_message)
        cif_pattern = re.compile(self.validation_pattern)
        if not cif_pattern.fullmatch(attr_value):
            self.error_message = "Invalid CIF format"
            raise EnterpriseManagementException(self.error_message)


        control_letter = attr_value[0]
        numeric_part = attr_value[1:8]
        control_character = attr_value[8]

        even_position_sum = 0
        odd_position_sum = 0

        for index in range(len(numeric_part)):
            if index % 2 == 0:
                doubled_value = int(numeric_part[index]) * 2
                if doubled_value > 9:
                    even_position_sum = even_position_sum + (doubled_value // 10) + (doubled_value % 10)
                else:
                    even_position_sum = even_position_sum + doubled_value
            else:
                odd_position_sum = odd_position_sum + int(numeric_part[index])

        total_sum = even_position_sum + odd_position_sum
        unit_digit = total_sum % 10
        base_digit = 10 - unit_digit

        if base_digit == 10:
            base_digit = 0

        control_letter_map = "JABCDEFGHI"

        if control_letter in ('A', 'B', 'E', 'H'):
            if str(base_digit) != control_character:
                self.error_message = "Invalid CIF character control number"
                raise EnterpriseManagementException(self.error_message)
        elif control_letter in ('P', 'Q', 'S', 'K'):
            if control_letter_map[base_digit] != control_character:
                self.error_message = "Invalid CIF character control letter"
                raise EnterpriseManagementException(self.error_message)

        else:
            self.error_message = "CIF type not supported"
            raise EnterpriseManagementException(self.error_message)
        return attr_value
