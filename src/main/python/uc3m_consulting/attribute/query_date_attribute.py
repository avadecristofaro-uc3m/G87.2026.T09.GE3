"""Class for query date validation"""
from datetime import datetime

from uc3m_consulting.attribute.attribute import Attribute
from uc3m_consulting.enterprise_management_exception import EnterpriseManagementException


class QueryDateAttribute(Attribute):
    """Class for validating query dates"""

    def __init__(self, attr_value):
        super().__init__()
        self.error_message = "Invalid date format"
        self.validation_pattern = r"^(([0-2]\d|3[0-1])\/(0\d|1[0-2])\/\d\d\d\d)$"
        self._attr_value = self.validate(attr_value)

    def validate(self, _attr_value):
        """Validate query date format and calendar correctness"""
        super().validate(_attr_value)
        try:
            datetime.strptime(_attr_value, "%d/%m/%Y").date()
        except ValueError as exception:
            raise EnterpriseManagementException("Invalid date format") from exception
        return _attr_value

    @property
    def value(self):
        """Return validated date value"""
        return self._attr_value
