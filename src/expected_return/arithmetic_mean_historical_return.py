from src.common.execution_time_recorder import ExecutionTimeRecorder
from src.expected_return.expected_returns_base import ExpectedReturnBase
from pypfopt import expected_returns


# Derived class for Mean Historical Return
class ArithmeticMeanHistoricalReturn(ExpectedReturnBase):
    @ExecutionTimeRecorder(module_name=__name__)  # Use __name__ t
    def _calculate_expected_return(self):
        ticker_expected_return_dict = expected_returns.mean_historical_return(self.data,
                                                                              returns_data=False,
                                                                              compounding=False)
        return self._convert_to_dataframe(ticker_expected_return_dict)
