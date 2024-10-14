import pandas as pd

from plugIn.common.execution_time_recorder import ExecutionTimeRecorder
from plugIn.optimization.riskfolio_lib_frontier import RiskFolioOptimizer


class WRRiskFolioOptimizer(RiskFolioOptimizer):
    @ExecutionTimeRecorder(module_name=__name__)
    def __init__(self, expected_returns, covariance_matrix, data: pd.DataFrame):
        super().__init__(expected_returns, covariance_matrix, data, rm='WR')
