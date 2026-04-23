"""Parent class for attributes"""
import re
from uc3m_consulting.enterprise_management_exception import EnterpriseManagementException

class Attribute():
    """Class for attributes"""
    def __init__(self):
        self._attr_value = ""
        self.error_message = ""
        self.validation_pattern = r""

    def validate(self,value):
        """Validate attribute value"""
        myregex= re.compile(self.validation_pattern)
        res = myregex.fullmatch(value)
        if not res:
            raise EnterpriseManagementException(self.error_message)
        return value

    @property
    def value(self):
        """Return attribute value"""
        return self._attr_value

    @value.setter
    def value(self,attr_value):
        """Set attribute value"""
        self._attr_value = attr_value
