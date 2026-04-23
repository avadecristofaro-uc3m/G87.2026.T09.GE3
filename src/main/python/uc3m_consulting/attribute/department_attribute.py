from .attribute import Attribute

class department_attribute(Attribute):
    def __init__(self, attr_value):
        self.validation_pattern = r"(HR|FINANCE|LEGAL|LOGISTICS)"
        self.error_message = "Invalid department"
        self._attr_value = super().validate(attr_value)   # store actual string

    @property
    def value(self):
        return self._attr_value