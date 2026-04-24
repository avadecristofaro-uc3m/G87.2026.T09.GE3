"""Class for validating department"""
from uc3m_consulting.attribute.attribute import Attribute

class DepartmentAttribute(Attribute):
    """Class for department attribute"""
    def __init__(self, attr_value):
        super().__init__()
        self.error_message = "Invalid department"
        self.validation_pattern = r"(HR|FINANCE|LEGAL|LOGISTICS)"
        self._attr_value = attr_value
        super().validate(attr_value)

    @property
    def value(self):
        """Return department attribute value"""
        return self._attr_value
