import collections

import numpy as np
from sympy.printing.tests.test_cupy import cp

from plugIn.common.execution_time_recorder import ExecutionTimeRecorder
from plugIn.processing_weight.allocationBase import AllocationBase


class MinRiskLpPortfolio(AllocationBase):
    def __init__(self, weights, latest_prices, total_portfolio_value=10000, short_ratio=None):
        super().__init__(weights, latest_prices, total_portfolio_value, short_ratio)

    @ExecutionTimeRecorder(module_name=__name__)
    def get_allocation(self, reinvest=False, verbose=False, solver="ECOS_BB"):
        """
        Convert continuous weights into a discrete portfolio allocation
        by minimizing portfolio variance (risk) using linear programming.

        This method minimizes the portfolio risk subject to budget constraints.

        :param reinvest: whether or not to reinvest cash gained from shorting
        :type reinvest: bool, defaults to False
        :param verbose: print error analysis?
        :type verbose: bool, defaults to False
        :param solver: the CVXPY solver to use (must support mixed-integer programs)
        :type solver: str, defaults to "ECOS_BB"
        :return: the number of shares of each ticker that should be purchased,
                 along with the amount of funds leftover.
        :rtype: (dict, float)
        """
        p = self.latest_prices.values
        n = len(p)
        w = np.fromiter([i[1] for i in self.weights], dtype=float)

        # Assume covariance matrix is identity for now (can be modified later)
        cov_matrix = np.eye(n)

        # Integer allocation
        x = cp.Variable(n, integer=True)
        # Remaining dollars
        r = self.total_portfolio_value - p.T @ x

        # Minimize variance (risk) of the portfolio
        risk = cp.quad_form(x, cov_matrix)
        constraints = [x >= 0, r >= 0]  # long only constraints

        opt = cp.Problem(cp.Minimize(risk), constraints)
        opt.solve(solver=solver)

        if opt.status not in {"optimal", "optimal_inaccurate"}:
            raise ValueError("Linear program failed to find a solution.")

        self.allocation = self._remove_zero_positions(
            collections.OrderedDict(zip([i[0] for i in self.weights], x.value.astype(int)))
        )

        if verbose:
            print("Funds remaining: {:.2f}".format(r.value))
            self._allocation_rmse_error(verbose)
        return self.allocation, r.value
