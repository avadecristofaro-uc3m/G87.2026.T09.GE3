"""Class for validating the CIF"""
import re
from uc3m_consulting.enterprise_management_exception import EnterpriseManagementException
from uc3m_consulting.attribute.attribute import Attribute

class CifAttribute(Attribute):
    """class for CIF attribute"""
    def __init__(self, attr_value):
        super().__init__()
        self.error_message = ""
        self.validation_pattern = r"^[ABCDEFGHJKNPQRSUVW]\d{7}[0-9A-J]$"
        self.attr_value = self.validate(attr_value)

    def validate(self, value):
        """validates cif attribute"""
        if not isinstance(value, str):
            self.error_message = "CIF code must be a string"
            raise EnterpriseManagementException(self.error_message)
        cif_pattern = re.compile(self.validation_pattern)
        if not cif_pattern.fullmatch(value):
            self.error_message = "Invalid CIF format"
            raise EnterpriseManagementException(self.error_message)


        control_letter = value[0]
        numeric_part = value[1:8]
        control_character = value[8]

        base_digit = self._calculate_control_digit(numeric_part)

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
        return value

    @staticmethod
    def _calculate_control_digit(numeric_part):
        """Calculate CIF control digit"""
        even_position_sum = 0
        odd_position_sum = 0

        for index, digit in enumerate(numeric_part):
            if index % 2 == 0:
                doubled_value = int(digit) * 2
                even_position_sum += sum(int(number) for number in str(doubled_value))
            else:
                odd_position_sum += int(digit)

        total_sum = even_position_sum + odd_position_sum
        base_digit = 10 - (total_sum % 10)

        if base_digit == 10:
            return 0

        return base_digit
