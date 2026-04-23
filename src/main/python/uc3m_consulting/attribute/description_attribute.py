"""Class for validating description"""
from .attribute import Attribute

class DescriptionAttribute(Attribute):
    """Class for description attribute"""
    def __init__(self, attr_value):
        self.validation_pattern = r"^.{10,30}$"
        self.error_message = "Invalid description format"
        super().validate(attr_value)
        self._attr_value = attr_value

    @property
    def value(self):
        """Return description attribute"""
        return self._attr_value
