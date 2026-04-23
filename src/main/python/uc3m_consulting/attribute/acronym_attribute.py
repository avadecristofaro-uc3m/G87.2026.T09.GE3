"""Class for acronym validation"""
from .attribute import Attribute

class AcronymAttribute(Attribute):
    """Class for acronym attribute"""
    def __init__(self, attr_value):
        self.validation_pattern = r"^[a-zA-Z0-9]{5,10}$"
        self.error_message = "Invalid acronym"
        super().validate(attr_value)
        self._attr_value = attr_value

    @property
    def value(self):
        """Return acronym value"""
        return self._attr_value
