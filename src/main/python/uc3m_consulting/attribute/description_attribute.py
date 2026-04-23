from .attribute import Attribute

class description_attribute(Attribute):
    def __init__(self, attr_value):
        self.validation_pattern = r"^.{10,30}$"
        self.error_message = "Invalid description format"
        self._attr_value = super().validate(attr_value)   # store actual string

    @property
    def value(self):
        return self._attr_value