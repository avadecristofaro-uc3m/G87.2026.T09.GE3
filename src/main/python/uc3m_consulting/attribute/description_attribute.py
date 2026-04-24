"""Class for validating description"""
from uc3m_consulting.attribute.attribute import Attribute

class DescriptionAttribute(Attribute):
    """Class for description attribute"""
    def __init__(self, attr_value):
        super().__init__()
        self.error_message = "Invalid description format"
        self.validation_pattern = r"^.{10,30}$"
        self._attr_value = attr_value
        super().validate(attr_value)

    @property
    def value(self):
        """Return description attribute"""
        return self._attr_value
