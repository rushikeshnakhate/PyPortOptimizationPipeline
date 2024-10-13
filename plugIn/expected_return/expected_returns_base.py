from abc import ABC, abstractmethod
from pypfopt import expected_returns


# Base class for expected returns
class ExpectedReturnBase(ABC):
    def __init__(self, data):
        self.data = data

    @abstractmethod
    def calculate_expected_return(self):
        pass

