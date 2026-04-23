"""Class for validating department"""
from .attribute import Attribute

class DepartmentAttribute(Attribute):
    """Class for department attribute"""
    def __init__(self, attr_value):
        self.validation_pattern = r"(HR|FINANCE|LEGAL|LOGISTICS)"
        self.error_message = "Invalid department"
        super().validate(attr_value)
        self._attr_value = attr_value

    @property
    def value(self):
        """Return department attribute value"""
        return self._attr_value
