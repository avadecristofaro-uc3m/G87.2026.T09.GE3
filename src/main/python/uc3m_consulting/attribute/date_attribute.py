from .attribute import Attribute
from uc3m_consulting.enterprise_management_exception import EnterpriseManagementException
from datetime import datetime, timezone

class date_attribute(Attribute):
    def __init__(self, attr_value):
        self.validation_pattern = r"^(([0-2]\d|3[0-1])\/(0\d|1[0-2])\/\d\d\d\d)$"
        self.error_message = "Invalid date format"
        self._attr_value = self.validate(attr_value)

    def validate(self, attr_value):
        super().validate(attr_value)
        try:
            my_date = datetime.strptime(attr_value, "%d/%m/%Y").date()
        except ValueError as exception:
            raise EnterpriseManagementException("Invalid date format") from exception

        if my_date < datetime.now(timezone.utc).date():
            raise EnterpriseManagementException("Project's date must be today or later.")

        if my_date.year < 2025 or my_date.year > 2050:
            raise EnterpriseManagementException("Invalid date format")
        return attr_value

    @property
    def value(self):
        return self._attr_value



