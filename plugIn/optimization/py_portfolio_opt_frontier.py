from plugIn.common.execution_time_recorder import ExecutionTimeRecorder
from plugIn.optimization.py_portfolio_opt_frontier_base import PyPortfolioOptFrontierBase


class PyPortfolioOptFrontier(PyPortfolioOptFrontierBase):
    @ExecutionTimeRecorder(module_name=__name__)
    def __init__(self, expected_returns, covariance_matrix, expected_return_type, risk_return_type, output_dir=None,
                 data=None):
        # Call the base class with default weight bounds (0, 1)
        super().__init__(expected_returns, covariance_matrix, expected_return_type, risk_return_type, output_dir, data,
                         weight_bounds=(0, 1))
