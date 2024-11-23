import pandas as pd

from src.common.execution_time_recorder import ExecutionTimeRecorder
from src.optimization.riskfolio_lib_frontier import RiskFolioOptimizer


class ADDRiskFolioOptimizer(RiskFolioOptimizer):
    @ExecutionTimeRecorder(module_name=__name__)  # Use __name__ to get the module name
    def __init__(self, expected_returns, covariance_matrix, expected_return_type, risk_return_type, output_dir,
                 data: pd.DataFrame):
        super().__init__(expected_returns, covariance_matrix, expected_return_type, risk_return_type, output_dir, data,
                         rm='ADD')
