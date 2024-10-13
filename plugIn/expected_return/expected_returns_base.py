from abc import ABC, abstractmethod
from pypfopt import expected_returns

from plugIn.common.execution_time_recorder import ExecutionTimeRecorder


# Base class for expected returns
class ExpectedReturnBase(ABC):
    def __init__(self, data):
        self.data = data

    @abstractmethod
    def calculate_expected_return(self):
        pass
