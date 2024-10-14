from plugIn.common.execution_time_recorder import ExecutionTimeRecorder
from plugIn.optimization.py_portfolio_opt_frontier_base import PyPortfolioOptFrontierBase


class PyPortfolioOptFrontierWithShortPosition(PyPortfolioOptFrontierBase):
    @ExecutionTimeRecorder(module_name=__name__)
    def __init__(self, expected_returns, covariance_matrix, data=None):
        # Call the base class with weight bounds allowing short positions (-1, 1)
        super().__init__(expected_returns, covariance_matrix, data, weight_bounds=(-1, 1))
