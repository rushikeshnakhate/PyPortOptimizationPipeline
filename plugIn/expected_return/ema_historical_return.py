from plugIn.expected_return.expected_returns_base import ExpectedReturnBase
from pypfopt import expected_returns

# Derived class for EMA Historical Return
class EMAHistoricalReturn(ExpectedReturnBase):
    def calculate_expected_return(self):
        return expected_returns.ema_historical_return(self.data)
