from plugIn.expected_return.expected_returns_base import ExpectedReturnBase
from pypfopt import expected_returns


# Derived class for Mean Historical Return
class CAGRMeanHistoricalReturn(ExpectedReturnBase):
    def calculate_expected_return(self):
        return expected_returns.mean_historical_return(self.data)