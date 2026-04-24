"""Class for acronym validation"""
from uc3m_consulting.attribute.attribute import Attribute

class AcronymAttribute(Attribute):
    """Class for acronym attribute"""
    def __init__(self, attr_value):
        super().__init__()
        self.error_message = "Invalid acronym"
        self.validation_pattern = r"^[a-zA-Z0-9]{5,10}$"
        self._attr_value = attr_value
        super().validate(attr_value)

    @property
    def value(self):
        """Return acronym value"""
        return self._attr_value
