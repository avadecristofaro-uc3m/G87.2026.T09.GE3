from .attribute import Attribute

class acronym_attribute(Attribute):
    def __init__(self, attr_value):
        self.validation_pattern = r"^[a-zA-Z0-9]{5,10}$"
        self.error_message = "Invalid acronym"
        self._attr_value = super().validate(attr_value)   # store actual string

    @property
    def value(self):
        return self._attr_value