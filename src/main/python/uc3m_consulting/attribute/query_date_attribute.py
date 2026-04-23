from datetime import datetime
from uc3m_consulting.enterprise_management_exception import EnterpriseManagementException
from .attribute import Attribute


class QueryDateAttribute(Attribute):
    """Class for validating query dates"""

    def __init__(self, attr_value):
        self.validation_pattern = r"^(([0-2]\d|3[0-1])\/(0\d|1[0-2])\/\d\d\d\d)$"
        self.error_message = "Invalid date format"
        self._attr_value = self.validate(attr_value)

    def validate(self, attr_value):
        """Validate query date format and calendar correctness"""
        super().validate(attr_value)
        try:
            datetime.strptime(attr_value, "%d/%m/%Y").date()
        except ValueError as exception:
            raise EnterpriseManagementException("Invalid date format") from exception
        return attr_value

    @property
    def value(self):
        """Return validated date value"""
        return self._attr_value