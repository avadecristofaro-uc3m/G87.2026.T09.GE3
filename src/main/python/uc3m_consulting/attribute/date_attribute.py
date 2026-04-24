"""Class for validating date"""
from datetime import datetime, timezone
from uc3m_consulting.enterprise_management_exception import EnterpriseManagementException
from uc3m_consulting.attribute.attribute import Attribute

class DateAttribute(Attribute):
    """Class for date attribute"""
    def __init__(self, attr_value):
        super().__init__()
        self.validation_pattern = r"^(([0-2]\d|3[0-1])\/(0\d|1[0-2])\/\d\d\d\d)$"
        self.error_message = "Invalid date format"
        self._attr_value = self.validate(attr_value)

    def validate(self, value):
        """Validate the date attribute"""
        super().validate(value)
        try:
            my_date = datetime.strptime(value, "%d/%m/%Y").date()
        except ValueError as exception:
            raise EnterpriseManagementException("Invalid date format") from exception

        if my_date < datetime.now(timezone.utc).date():
            raise EnterpriseManagementException("Project's date must be today or later.")

        if my_date.year < 2025 or my_date.year > 2050:
            raise EnterpriseManagementException("Invalid date format")
        return value

    @property
    def value(self):
        """Return the date attribute"""
        return self._attr_value
