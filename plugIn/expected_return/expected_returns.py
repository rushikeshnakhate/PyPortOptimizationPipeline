from abc import ABC, abstractmethod
from pypfopt import expected_returns


# Base class for expected returns
class ExpectedReturnBase(ABC):
    def __init__(self, data):
        self.data = data

    @abstractmethod
    def calculate_expected_return(self):
        pass


# Derived class for Mean Historical Return
class CAGRMeanHistoricalReturn(ExpectedReturnBase):
    def calculate_expected_return(self):
        return expected_returns.mean_historical_return(self.data)


# Derived class for Mean Historical Return
class ArithmeticMeanHistoricalReturn(ExpectedReturnBase):
    def calculate_expected_return(self):
        return expected_returns.mean_historical_return(self.data, returns_data=False, compounding=False)


# Derived class for EMA Historical Return
class EMAHistoricalReturn(ExpectedReturnBase):
    def calculate_expected_return(self):
        return expected_returns.ema_historical_return(self.data)


# Derived class for CAPM Return
class CAPMReturn(ExpectedReturnBase):
    def calculate_expected_return(self):
        return expected_returns.capm_return(self.data)


# Derived class for Time-Weighted Rate of Return (TWRR)
class TWRRReturn(ExpectedReturnBase):
    def calculate_expected_return(self):
        monthly_prices = self.data.resample('ME').last()
        monthly_returns = monthly_prices.pct_change()
        return (1 + monthly_returns).prod() - 1
