"""Class for budget validation"""
from uc3m_consulting.enterprise_management_exception import EnterpriseManagementException
from uc3m_consulting.attribute.attribute import Attribute

class BudgetAttribute(Attribute):
    """Class for budget attribute"""
    def __init__(self, attr_value):
        super().__init__()
        self.error_message= "Invalid budget amount"
        self.validation_pattern= r""
        self._attr_value= self.validate(attr_value)

    def validate(self, _attr_value):
        """Validate budget format and range, and return it as float."""
        try:
            budget_value = float(_attr_value)
        except ValueError as exc:
            raise EnterpriseManagementException(self.error_message) from exc

        budget_as_string = str(budget_value)
        if "." in budget_as_string:
            decimals_length = len(budget_as_string.split('.')[1])
            if decimals_length > 2:
                raise EnterpriseManagementException(self.error_message)

        if budget_value < 50000 or budget_value > 1000000:
            raise EnterpriseManagementException(self.error_message)

        return budget_value

    @property
    def value(self):
        """Return budget value"""
        return self._attr_value
