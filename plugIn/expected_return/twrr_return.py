from plugIn.expected_return.expected_returns_base import ExpectedReturnBase
from pypfopt import expected_returns

# Derived class for Time-Weighted Rate of Return (TWRR)
class TWRRReturn(ExpectedReturnBase):
    def calculate_expected_return(self):
        monthly_prices = self.data.resample('ME').last()
        monthly_returns = monthly_prices.pct_change()
        return (1 + monthly_returns).prod() - 1