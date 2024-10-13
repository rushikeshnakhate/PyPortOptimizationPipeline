from plugIn.expected_return.expected_returns_base import ExpectedReturnBase
from pypfopt import expected_returns


# Derived class for CAPM Return
class CAPMReturn(ExpectedReturnBase):
    def calculate_expected_return(self):
        return expected_returns.capm_return(self.data)
