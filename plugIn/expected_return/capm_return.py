from plugIn.common.execution_time_recorder import ExecutionTimeRecorder
from plugIn.expected_return.expected_returns_base import ExpectedReturnBase
from pypfopt import expected_returns


# Derived class for CAPM Return
class CAPMReturn(ExpectedReturnBase):
    @ExecutionTimeRecorder(module_name=__name__)  # Use __name__ t
    def _calculate_expected_return(self):
        return self._convert_to_dataframe(expected_returns.capm_return(self.data))
